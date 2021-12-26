import asyncio
import functools
import json
import logging
import operator
import sys
from concurrent.futures import ThreadPoolExecutor
from itertools import islice, takewhile, starmap, repeat
from operator import truth
from typing import List, Iterable, Union, TextIO, Optional
import boto3
import pandas as pd
import requests

logger = logging.getLogger()
logger.setLevel(logging.INFO)
formatter = logging.Formatter(fmt=' %(name)s :: %(levelname)s :: %(message)s')


class AWSClient():
    def __init__(self, api_url="your API URL",
                 lambda_arn="your lambda arn", max_worker: int = 10, chunk_size: int = 100,
                 log_filename: str = "awsclient.log"):

        self._lambda_client = boto3.client('lambda')
        self._api_url = api_url
        self._lambda_arn = lambda_arn
        self._max_worker = max_worker
        self._chunk_size = chunk_size


        # set stdout handler
        stdout_handler = logging.StreamHandler(sys.stdout)
        stdout_handler.setLevel(logging.INFO)
        stdout_handler.setFormatter(formatter)

        # set file handler
        file_handler = logging.FileHandler(log_filename)
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)

        # set handlers for logger
        logger.addHandler(file_handler)
        logger.addHandler(stdout_handler)

    @property
    def lambda_arn(self):
        return self._lambda_arn

    @lambda_arn.setter
    def lambda_arn(self, lambda_arn):
        self._lambda_arn = lambda_arn

    @property
    def api_url(self):
        return self._api_url

    @api_url.setter
    def api_url(self, api_url):
        self._api_url = api_url

    @property
    def max_worker(self):
        return self._max_worker

    @max_worker.setter
    def max_worker(self, max_worker):
        self._max_worker = max_worker

    @property
    def chunk_size(self):
        return self._chunk_size

    @chunk_size.setter
    def chunk_size(self, chunk_size):
        self._chunk_size = chunk_size

    @staticmethod
    def _chunks(iterable: Iterable, n=100):
        """
        separate the input interable into chunks, with the size of the chunk defined by n (default=100)
        This function uses generator to process items from input iterables with efficient memory usage
        :param iterable:   The input iterable tha will be separated into chunks
        :param n:          The size of each chunk
        :return:           a generator with multiple chunks
        """
        return takewhile(truth, map(tuple, starmap(islice, repeat((iter(iterable), n)))))

    def _fetch_rest_api(self, session, params: List) -> List:
        """
        This function send the input parameter to Rest API URL by HTTP POST
        :param session:     A requests session
        :param params:      Data sent to API for processing (List of strings)
        :return:            Processed results
        """
        with session.post(self._api_url, json.dumps(params)) as response:
            rs = response.text
            if response.status_code != 200:
                print("FAILURE FOR API::{}".format(self._api_url))
            return rs

    async def _get_results_by_api(self, input_data_blocks):
        """
        This coroutine invokes Rest API and send input data chunks using multi-threads
        in each thread, a chunk of data is sent to API
        :param input_data_blocks: a generator that can deliver data in chunks
        :return: list of the results
        """
        rs = []

        with ThreadPoolExecutor(max_workers=self._max_worker) as executor:
            with requests.Session() as session:
                loop = asyncio.get_event_loop()

                tasks = [
                    loop.run_in_executor(executor, self._fetch_rest_api, *(session, param))
                    for param in input_data_blocks
                ]
                for response in await asyncio.gather(*tasks):
                    rs.append(response)

        return rs

    def _fetch_lambda(self, params):
        """
        This function invoke aws lambda function synchronously and fetch the results
        :param params: List of input strings
        :return:       Processed results
        """
        payload = json.dumps({"queries": params})

        try:
            response = self._lambda_client.invoke(
                FunctionName=self._lambda_arn,
                InvocatonType='RequestResponse',
                Payload=bytes(payload, encoding='utf-8')
            )

            rs = json.load(response['Payload'])
            return rs
        except Exception as e:
            logger.error(e)
            return None

    async def _get_results_by_lambda(self, input_data_chunks):
        """
        This coroutine invokes Rest API and send input data chunks using multi-threads
        in each thread, a chunk of data is sent to API
        :param input_data_chunks: a generator that delivers data in chunks
        :return: list of the results
        """
        rs = []
        with ThreadPoolExecutor(max_workers=self._max_worker) as executor:
            loop = asyncio.get_event_loop()

            tasks = [
                loop.run_in_executor(
                    executor,
                    self._fetch_lambda,
                    param
                )
                for param in input_data_chunks
            ]
            for response in await asyncio.gather(*tasks):
                rs.append(response)

    def _get_lambda_multi_threads(self, input_params):
        """
        This function process the input_parameters by muti-threads using submit function
        and gather the Future object results as a list
        :param input_params:  A generator that delivers the data in chunks
        :return:              A list of results
        """
        with ThreadPoolExecutor(max_workers=self._max_worker) as executor:
            futures = []
            for param in input_params:
                payload = json.dumps({"queries": param})
                futures.append(
                    executor.submit(self._lambda_client.invoke,
                                    FunctionName=self._lambda_arn,
                                    InvocationType="RequestResponse",
                                    Payload=bytes(payload, encoding='utf-8')
                                    )
                )

        results = [json.load(future.result()['Payload']) for future in futures]
        return [item for sublist in results for item in sublist]

    def _call_rest_api(self, input_params):
        """
        This function calls the coroutine of self._get_results_by_api on input_params
        :param input_params: A generator delivering input data in chunks
        :return:             Return the list of results
        """
        loop = asyncio.get_event_loop()
        future = asyncio.ensure_future(self._get_results_by_api(input_params))
        return loop.run_until_complete(future)

    def _call_lambda(self, input_params):
        """
        This function calls the coroutine of self._get_results_by_lambda on input_params
        :param input_params: A generator delivering input data in chunks
        :return:             Return the list of results
        """
        loop = asyncio.get_event_loop()
        future = asyncio.ensure_future(self._get_results_by_lambda(input_params))
        return loop.run_until_complete(future)

    def request_by_lambda(self, messages: Union[List[str], TextIO], no_async: bool = False,
                          no_output: bool = False) -> Optional[pd.DataFrame]:
        """
        This function is used by users to invoke lambda function to process input data
        :param messages:  Input data, either in form of a list of strings, or an input file
        :param no_async:  Use async methods or not
        :param no_output: Return results or not
        :return:          Pandas DataFrame, or None
        """
        chunked_list = AWSClient._chunks(messages, self._chunk_size)

        if no_async:
            results = self._get_lambda_multi_threads(chunked_list)
        else:
            # concatenate sub-list to list
            results = functools.reduce(operator.iconcat, self._call_lambda(chunked_list), [])

        if no_output:
            return None
        else:
            return pd.DataFrame(results)

    def fetch_by_api(self, messages: Union[List[str], TextIO], no_output: bool = False) -> Optional[pd.DataFrame]:
        """
        This function is used by users to invoke Rest API to process input data
        :param messages:   Input data, either in form of a list of strings, or an input file
        :param no_output:  Return results or not
        :return:           Pandas DataFrame, or None
        """
        chunked_list = AWSClient._chunks(messages, self._chunk_size)
        results = functools.reduce(operator.iconcat, self._call_rest_api(chunked_list), [])

        if no_output:
            return None
        else:
            return pd.DataFrame(results)

if __name__ == "__main__":
    ac = AWSClient("api_url", "lambda_arn")

    print(ac.max_worker)
    print(ac.lambda_arn)
    print(ac.api_url)
    print(ac.chunk_size)
    ac.max_worker = 50
    ac.api_url = "api_url_2"
    ac.lambda_arn = "lambda2"
    ac.chunk_size = 100
    print(ac.max_worker)
    print(ac.lambda_arn)
    print(ac.api_url)
    print(ac.chunk_size)





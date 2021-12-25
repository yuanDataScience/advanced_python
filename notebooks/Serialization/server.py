"""Example gRPC weather server"""
import logging
from threading import Lock

# import the genrated python files
import weather_grpc_pb2 as pb
import weather_grpc_pb2_grpc as gpb

# use an in memory list as db
db = []
lock = Lock()


# implement WeatherServer class with AddTemperature function
# request is a Temperature object
class WeatherServer(gpb.WeatherServicer):
    def AddTemperature(self, request, context):
        with lock:
            logging.info('add: %r', request)
            db.append(request)
            record_count = len(db)
        return pb.AddReply(record_count=record_count)


if __name__ == '__main__':
    from concurrent.futures import ThreadPoolExecutor
    import grpc

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
    )

    # start the server
    server = grpc.server(ThreadPoolExecutor())
    # add service
    gpb.add_WeatherServicer_to_server(WeatherServer(), server)
    port = 8088
    # run on http (grpc default to run on https, so run insecure port)
    server.add_insecure_port(f'[::]:{port}')
    #start server
    server.start()
    logging.info(f'server ready on {port}')
    # wait for server termination
    server.wait_for_termination()

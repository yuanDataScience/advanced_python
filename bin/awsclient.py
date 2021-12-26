from aws_client.aws_client import AWSClient, Version

from docopt import docopt

if __name__ == "__main__":
    __doc__ =f"""awsclient.py v{Version}
    
    AWS client was designed as a client to send large amount of string messages to aws lambda functions for data processing.
    You need to have the access to the aws lambda function in order to invoke the lambda function by this tool. Or 
    you can invoke the Rest API by HTTP POST method if you have the Rest API url.
    lambda function can optional connect to an aws RDS database to store the calculated results to save computation resources
    when input message strings have been requested before. The only requirement for lambda function is that it needs to 
    extract the input message as a list of strings using event["queries"]. 
    
    Usage:
        awsclient.py -i=<str> [-o=<str> -e=<str> -w=<int> -n=<int> --no-async --no-output -v]
        
        -i=<str>                 input file containing messages for processing
        -o=<str>                 output file name. If not specified, results will be written to result.txt
        -e=<str>                 Error log. If not specified, will use the input filename as the prefix





"""





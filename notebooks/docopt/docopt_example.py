from docopt import docopt

if __name__ == "__main__":
    __doc__ = f"""
        This is a sample python file to demonstrate how to use docopt to define commandline user interfaces, including:
        how to define required fields with and without arguments
        how to define optional fields with and without arguments
        how docopt parses use input options
        
        Usage:
            docopt_example.py -i=<str> -m=<int> [-o=<str> -c=<int> -v]
            
        Options:
            -h, --help                           Show this screen
            -i, --input_file=<input_file>        Input file for the script
            -m, --message_id=<message_id>        Id of message
            -c, --chunk_size=<chunk_size>        Number of messages in each chunk
            -o, --output_file=<output_file>      Output file name (default: output.txt)
            -v, --verbose                        Verbose output if specified      
    """

    args = docopt(__doc__)

    output_file = "output.txt"
    chunk_size = 100
    verbose = False
    input_file = args["--input_file"]
    message_id = args["--message_id"]

    if args.get("--output"):
        output_file = args["--output"]
    if args.get('--verbose'):
        verbose = True
    if args.get("--chunk_size"):
        chunk_size = args["-chunk_size"]

    print(args)

import argparse
import os
from contextlib import redirect_stdout
from DependMLMoi import __version__

def parse_args():
    # Create the parser
    parser = argparse.ArgumentParser(description="Process some flags.")

    # Add the flags to the parser
    parser.add_argument('-n, --name', action='store_true', help='Sets the AUTO_INSTALL variable to True')
    parser.add_argument('--auto', action='store_true', help='Sets the AUTO_INSTALL variable to True')
    parser.add_argument('--debug', action='store_true', help='Sets the DEBUG variable to True')
    parser.add_argument('--logging', action='store_true', help='Sets the LOGGING variable to True')
    parser.add_argument('-q', '--quiet', action='store_true', help='Suppresses the output')
    parser.add_argument('-c', '--custom', action='store_true', help='add a custom library')
    parser.add_argument('-l', '--level', action='store_true', help='set logging level')
    parser.add_argument('-t', '--type', action='store_true', help='Type of App (LLM, ML, Web)')
    parser.add_argument('-v', '--version', action='version', version=f'%(prog)s {__version__}', help='Version of DependMLOps')

    # Parse the arguments
    args = parser.parse_args()

    # If '-q' or '--quiet' is set, suppress the output
    if args.custom:
        custom_list = []
        new_items = args.custom.split(',')
        custom_list.extend(new_items)

    if args.quiet:
        args.debug = None
        with open(os.devnull, 'w') as f:
            with redirect_stdout(f):
                print('This will not appear anywhere')

    return args

        










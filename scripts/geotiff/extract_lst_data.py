import argparse
import logging
from utilities import lib

parser = argparse.ArgumentParser(description='Extract masked data from a geotiff.')
parser.add_argument('-i', '--input', help="Input geotiff.", required=True)
parser.add_argument('-q', '--quality', help="Quality geotiff.", required=True)
parser.add_argument('-x', '--dry-run', help="List the files to be processed but don't take any statistics.",
                    action="store_true")
parser.add_argument('-v', '--verbose', help="Verbose run.", action="store_true")
parser.add_argument('-b', '--log-file', help="Name of the file to log info and warnings.")
parser.add_argument('-z', '--sanity-path', help="Save mask to the specified directory.")
args = parser.parse_args()

if args.verbose and args.log_file is not None:
    logging.basicConfig(level=logging.DEBUG, filename=args.log_file)
elif args.verbose and args.log_file is None:
    logging.basicConfig(level=logging.DEBUG)

data = lib.create_lst_masked_array(args.input, args.quality, args.sanity_path)
for idx, val in enumerate(data.flatten()):
    print str(val * .02)


import argparse
from rain_lib import *
"""
With this file, I decided to keep the modis dating conventions.
"""
parser = argparse.ArgumentParser(description='Acquire rain data from the SSMI.')
parser.add_argument('-s', '--start-year', help='YYYY', required=True, type=int)
parser.add_argument('-e', '--end-year', help='YYYY', required=True, type=int)
parser.add_argument('-f', '--first-day', help='ddd', required=True)
parser.add_argument('-l', '--last-day', help='ddd', required=True)
parser.add_argument('-d', '--directory-path', help='Path to directory containing the data.', required=True)
parser.add_argument('-v', '--verbose', help="Verbose run.", action="store_true")
parser.add_argument('-b', '--log-file', help="Name of the file to log info and warnings.")
args = parser.parse_args()

if args.verbose and args.log_file is not None:
    logging.basicConfig(level=logging.DEBUG, filename=args.log_file)
elif args.verbose and args.log_file is None:
    logging.basicConfig(level=logging.DEBUG)

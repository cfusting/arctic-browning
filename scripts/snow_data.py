import argparse
from lib import *
import modisSuite
DATE_FORMAT = '%Y.%m.%d'

parser = argparse.ArgumentParser(description='Download MODIS snow data .')
parser.add_argument('-s', '--start-day', help='YYYY.MM.DD', required=True)
parser.add_argument('-e', '--end-day', help='YYYY.MM.DD', required=True)
parser.add_argument('-d', '--directory', help='Path to directory for storing the data.', required=True)
parser.add_argument('-t', '--tiles', nargs='+', help='tiles you would like to download, format as python list',
                    required=True)
parser.add_argument('-v', '--verbose', help="Verbose run.", action="store_true")
parser.add_argument('-b', '--log-file', help="Name of the file to log info and warnings.")
args = parser.parse_args()

if args.verbose and args.log_file is not None:
    logging.basicConfig(level=logging.DEBUG, filename=args.log_file)
elif args.verbose and args.log_file is None:
    logging.basicConfig(level=logging.DEBUG)

end_date = datetime.strptime(args.end_day, DATE_FORMAT)
start_date = datetime.strptime(args.start_day, DATE_FORMAT)
duration = end_date - start_date
d = duration.days

username = "tim_stevens"
password = "cowDuck!37"
product = "MOD10A2.006"

doo = modisSuite.downloader(product, username, password, date=args.start_day, delta=d, tuiles=args.tiles,
                            output=args.directory)
for x, y in doo.telechargerTout():
    print(x, y)

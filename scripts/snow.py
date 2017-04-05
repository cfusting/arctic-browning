import argparse
from lib import *

parser = argparse.ArgumentParser(description='Fetch temporal statistics from a list of rasters.')
parser.add_argument('-s', '--start-year', help='YYYY', required=True, type=int)
parser.add_argument('-e', '--end-year', help='YYYY', required=True, type=int)
parser.add_argument('-f', '--first-day', help='ddd', required=True)
parser.add_argument('-l', '--last-day', help='ddd', required=True)
parser.add_argument('-d', '--directory-path', help='Path to directory containing the data.', required=True)
parser.add_argument('-k', '--data-file-regex', help='Filter files using this expression. Make sure to wrap this in'
                                                    ' single quotes.', required=True)
parser.add_argument('-o', '--output-file', help='file to output list to. include directory path. default is sys.out')
parser.add_argument('-j', '--date-regex', help='Extract the date using this expression. Make sure to wrap this in '
                                               'single quotes.', required=True)
parser.add_argument('-n', '--no-space', help='Do not aggregate over space.', action='store_true')
parser.add_argument('-x', '--dry-run', help="List the files to be processed but don't take any statistics.",
                    action="store_true")
parser.add_argument('-v', '--verbose', help="Verbose run.", action="store_true")
parser.add_argument('-c', '--no-check', help="Don't check that the data and reliability files match up. This could "
                                             "result in the wrong mask being created.")
parser.add_argument('-b', '--log-file', help="Name of the file to log info and warnings.")
parser.add_argument('-z', '--sanity-path', help="Save masks to specified directory.")
args = parser.parse_args()

if args.verbose and args.log_file is not None:
    logging.basicConfig(level=logging.DEBUG, filename=args.log_file)
elif args.verbose and args.log_file is None:
    logging.basicConfig(level=logging.DEBUG)

snow_files = get_files_list(args.directory_path, args.data_file_regex, args.date_regex)
snow_files_in_range = []
for year in range(args.start_year, args.end_year + 1):
    snow_files_in_range.append(filter_data_files_in_range(snow_files, year, args.first_day, args.last_day))

if args.output_file:
    output = open(args.output_file, 'w')
    for filename in snow_files_in_range:
        output.write("%s\n" % filename)
else:
    for filename in snow_files_in_range:
        print("%s\n" % filename)




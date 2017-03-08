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
parser.add_argument('-r', '--reliability-file-regex', help='Filter files using this expression. Make sure to wrap this'
                                                           ' in single quotes.', required=True)
parser.add_argument('-j', '--date-regex', help='Extract the date using this expression. Make sure to wrap this in '
                                               'single quotes.', required=True)
parser.add_argument('-o', '--out-path', help="Output file path.", required=True)
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

data_files, reliability_files = get_data_and_reliability_lists(args.directory_path, args.data_file_regex,
                                                               args.date_regex, args.reliability_file_regex)

validate_reliability(data_files, reliability_files, args.date_regex)
masked_props = []
for year in range(args.start_year, args.end_year + 1):
    data_files_in_range, reliability_files_in_range = filter_files_in_range(data_files, reliability_files, year,
                                                                            args.first_day, args.last_day,
                                                                            args.date_regex)
    space_time = retrieve_lst_space_time(data_files_in_range, reliability_files_in_range,
                                     args.date_regex, args.sanity_path)
    unmasked_props = get_unmasked_pixel_proportion_over_time(space_time)
    logging.debug("Unmasked Pixels for one year shape :" + str(unmasked_props.shape))
    masked_props.append(unmasked_props)

masked_props_over_years = np.stack(masked_props, axis=TIME_AXIS).mean(axis=TIME_AXIS)
masked_out = (masked_props_over_years * 10000).astype(int)
logging.debug("Output shape: " + str(masked_out.shape))
# Assumes all files are of the same dimension. Safe assumption but shitty way to do this.
save_like_geotiff(data_files[0], np.int16, masked_out, args.out_path)


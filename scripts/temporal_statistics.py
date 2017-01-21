import re
import os
import gdal
import argparse
import numpy as np
import numpy.ma as ma
import sys
import logging
from lib import build_qa_mask
from datetime import datetime

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
parser.add_argument('-x', '--dry-run', help="List the files to be processed but don't take any statistics.",
                    action="store_true")
parser.add_argument('-v', '--verbose', help="Verbose run.", action="store_true")
parser.add_argument('-c', '--no-check', help="Don't check that the data and reliability files match up. This could "
                                             "result in the wrong mask being created.")
parser.add_argument('-b', '--log-file', help="Name of the file to log info and warnings.")
args = parser.parse_args()

logger = logging.getLogger(__name__)
format_handler = logging.Formatter(fmt="%(asctime)s %(message)s")
logger.addHandler(format_handler)
if args.verbose:
    logger.setLevel(logging.DEBUG)
if args.log_file is not None:
    file_handler = logging.FileHandler(args.log_file)
    logger.addHandler(file_handler)

TIME_AXIS = 2
YEAR_DAY = "%Y%j"


def get_filenames_list(file_name):
    with open(file_name) as dat:
        data_files = dat.readlines()
        data_files = [dat.strip() for dat in data_files]
        return data_files


def open_raster_file(file_name, array_type):
    rast = gdal.Open(file_name)
    band = rast.GetRasterBand(1)
    return np.array(band.ReadAsArray(), array_type)


def create_masked_array(array_file, array_type, mask_file, mask_type):
    raster_array = open_raster_file(array_file, array_type)
    rel_array = open_raster_file(mask_file, mask_type)
    build_qa_mask(raster_array, rel_array)
    return ma.array(raster_array, mask=rel_array)


def get_files_in_time_range(start, end, files, date_regex):
    filtered_files = []
    for fl in files:
        fl_time = re.compile(date_regex).search(fl).group()
        file_datetime = datetime.strptime(fl_time, YEAR_DAY)
        if file_datetime is not None and start <= file_datetime <= end:
            filtered_files.append(fl)
    return filtered_files


def get_matching_files(directory, file_regex):
    files = os.listdir(directory)
    names = filter(lambda x: re.compile(file_regex).search(x) is not None, files)
    return map(lambda x: directory + os.sep + x, names)

logger.debug("Will match date with: " + args.date_regex)
data_files = get_matching_files(args.directory_path, args.data_file_regex)
data_files.sort(reverse=True)
logger.debug("Matched data files:")
for i in data_files:
    logger.debug(i)
reliability_files = get_matching_files(args.directory_path, args.reliability_file_regex)
reliability_files.sort(reverse=True)
logger.debug("Matched reliability files:")
for i in reliability_files:
    logger.debug(i)
date_pattern = re.compile(args.date_regex)
for raster, rel in zip(data_files, reliability_files):
    if date_pattern.search(raster).group() != date_pattern.search(rel).group():
        sys.exit("Data and reliability files do not match.")
logger.info("Validated that each data file has an associated reliability file.")
for year in range(args.start_year, args.end_year + 1):
    start_date = datetime.strptime(str(year) + args.first_day, YEAR_DAY)
    end_date = datetime.strptime(str(year) + args.last_day, YEAR_DAY)
    data_files_in_range = get_files_in_time_range(start_date, end_date, data_files, args.date_regex)
    reliability_files_in_range = get_files_in_time_range(start_date, end_date, reliability_files, args.date_regex)
    space_list = []
    for raster, rel in zip(data_files_in_range, reliability_files_in_range):
        if date_pattern.search(raster).group() != date_pattern.search(rel).group():
            sys.exit("Data and reliability files do not match.")
        logger.info("Processing data: " + raster)
        logger.info("Applying reliability mask: " + rel)
        masked_array = create_masked_array(raster, np.int16, rel, np.int8)
        logger.debug("Data totally masked: " + str(masked_array.mask.all()))
        space_list.append(masked_array)
    # Lon, Lat, Time.
    space_time = ma.dstack(space_list)
    logger.debug("Space-time shape:" + str(space_time.shape))
    logger.debug("Space-time totally masked: " + str(space_time.mask.all()))
    if args.dry_run is False:
        # Average over time, then over space.
        mean_dat = space_time.mean(axis=TIME_AXIS).mean()
        sd_dat = space_time.std(axis=TIME_AXIS).mean()
        min_dat = space_time.min(axis=TIME_AXIS).mean()
        max_dat = space_time.max(axis=TIME_AXIS).mean()
        print str(year) + "," + str(mean_dat) + "," + str(min_dat) + "," + str(max_dat) + "," + str(sd_dat)

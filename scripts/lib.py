import re
import os
import gdal
import numpy as np
import numpy.ma as ma
import sys
import logging
from datetime import datetime
from QA_check import qa_check
import gdal_lib as gd

TIME_AXIS = 2
YEAR_DAY = "%Y%j"
NO_DATA = -3000


def build_qa_mask(iarray, rarray):
    """build an array mask.

    :param iarray: input arrray (ndvi)
    :param rarray: reliability array. Resulting mask is stored here.
    :return:
    """
    # rarray[rarray == 1] = 0
    rarray[iarray == NO_DATA] = 1
    rarray[rarray != 0] = 1


def mask_missing(raster_array, mask):
    mask[raster_array == NO_DATA] = True


def build_mask(raster_array, rel_array):
    mask = qa_check(rel_array)
    mask = np.logical_not(mask)
    mask_missing(raster_array, mask)
    return mask


def get_filenames_list(file_name):
    with open(file_name) as dat:
        data_files = dat.readlines()
        data_files = [dat.strip() for dat in data_files]
        return data_files


def open_raster_file(file_name, array_type):
    """
    Take Modis VI data and convert it into a numpy array of array_type.
    :param file_name: Name of the file.
    :param array_type: Type of the array.
    :return: Numpy array
    """
    rast = gdal.Open(file_name)
    band = rast.GetRasterBand(1)
    return np.array(band.ReadAsArray(), array_type), rast


def create_masked_array(array_file, array_type, mask_file, mask_type, sanity_path):
    raster_array, srcds = open_raster_file(array_file, array_type)
    rel_array, srcds2 = open_raster_file(mask_file, mask_type)
    mask = build_mask(raster_array, rel_array)
    if sanity_path is not None:
        driver = gdal.GetDriverByName("GTiff")
        ndv, xsize, ysize, geot, projection, datatype = gd.get_geo_info(srcds)
        gd.create_geotiff(sanity_path + os.sep + "_mask" + array_file, mask, driver, ndv, NO_DATA, xsize, ysize, geot,
                          projection, datatype)
    return ma.array(raster_array, mask=mask)


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


def get_data_and_reliability_lists(directory_path, data_file_regex, date_regex, reliability_file_regex):
    logging.debug("Will match date with: " + date_regex)
    data_files = get_matching_files(directory_path, data_file_regex)
    data_files.sort(reverse=True)
    logging.debug("Matched data files:")
    for i in data_files:
        logging.debug(i)
    reliability_files = get_matching_files(directory_path, reliability_file_regex)
    reliability_files.sort(reverse=True)
    logging.debug("Matched reliability files:")
    for i in reliability_files:
        logging.debug(i)
    return data_files, reliability_files


def validate_reliability(data_files, reliability_files, date_regex):
    for raster, rel in zip(data_files, reliability_files):
        if re.compile(date_regex).search(raster).group() != re.compile(date_regex).search(rel).group():
            sys.exit("Data and reliability files do not match.")
    logging.info("Validated that each data file has an associated reliability file.")


def filter_files_in_range(data_files, reliability_files, year, first_day, last_day, date_regex):
    start_date = datetime.strptime(str(year) + first_day, YEAR_DAY)
    end_date = datetime.strptime(str(year) + last_day, YEAR_DAY)
    return (get_files_in_time_range(start_date, end_date, data_files, date_regex),
            get_files_in_time_range(start_date, end_date, reliability_files, date_regex))


def retrieve_space_time(data_files, reliability_files, date_regex, sanity_path):
    space_list = []
    for raster, rel in zip(data_files, reliability_files):
        if re.compile(date_regex).search(raster).group() != re.compile(date_regex).search(rel).group():
            sys.exit("Data and reliability files do not match.")
        logging.info("Processing data: " + raster)
        logging.info("Applying reliability mask: " + rel)
        masked_array = create_masked_array(raster, np.int16, rel, np.int8, sanity_path)
        logging.warn("Data totally masked: " + str(masked_array.mask.all()))
        space_list.append(masked_array)
    # Lon, Lat, Time.
    space_time = ma.dstack(space_list)
    logging.debug("Space-time shape:" + str(space_time.shape))
    logging.warn("Space-time totally masked: " + str(space_time.mask.all()))
    return space_time


def average_over_time(space_time):
    return (space_time.mean(axis=TIME_AXIS),
            space_time.count(axis=TIME_AXIS) /
            float(space_time.shape[TIME_AXIS]))


def average_over_time_then_space(space_time):
    space, weight = average_over_time(space_time)
    space_masked = ma.masked_less(space, 1200)
    weight_masked = ma.array(weight, mask=space_masked.mask)
    return space_masked.mean(), weight_masked.mean()

import re
import os
import gdal
import numpy as np
import numpy.ma as ma
import sys
import logging
from datetime import datetime
from lib import *
import gdal_lib as gd
"""
In order to help with complexity, I created this file to separate SSMI processing from MODIS processing
"""
YEAR_DAY = "%Y%j"
YEAR_MONTH_DAY = "%Y%m%d"


def get_files_list(file_path, start_year, end_year, first_day, last_day):
    """
    :param file_path: where the file things are
    :param start_year: the beginning of the files we want
    :param end_year: the end of them
    :param first_day: start of study each year
    :param last_day: end of study each year
    :return: a list of the files that are included in the given ranges
    """
    dat = get_filenames_list(file_path)
    files = []
    for year in range(start_year, end_year, 1):
        start = datetime.strptime(str(year) + first_day, YEAR_DAY)
        end = datetime.strptime(str(year) + last_day, YEAR_DAY)
        files.append(get_files_over_time(dat, start, end))
    return files


def get_files_over_time(file_list, start, end):
    return {x for x in file_list if start <= get_date_time(x) <= end}


def convert_date(year, day):
    """

    :param year: the year of said date
    :param day: the day of said date
    :return: the date in question in YYYYMMDD format
    """
    date = datetime.strptime("{}{}".format(year, day), YEAR_DAY)
    return date.strftime(YEAR_MONTH_DAY)


def get_date_time(file_name):
    """

    :param file_name: the name of the file
    :return: the datetime object of that file
    """
    date = file_name[4:12]
    return datetime.strptime(date, YEAR_MONTH_DAY)

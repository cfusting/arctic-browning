import logging
import ntpath
import re
from functools import partial

import numpy
from pyhdf.SD import SD

import design_matrix as dm
from utilities.design_matrix import get_simple_variable_names


class LearningData:
    DEFAULT_PREFIX = 'ARG'
    CSV = "csv"

    def __init__(self):
        self.num_variables = None
        self.num_observations = None
        self.predictors = None
        self.response = None
        self.variable_names = None
        self.variable_prefixes = None
        self.unique_variable_prefixes = None
        self.variable_type_indices = None
        self.variable_dict = None
        self.name = None
        self.design_matrix = None
        self.data_attributes = {}

    def from_file(self, file_name, header=False):
        file_type = file_name[-3:]
        if file_type == "hdf":
            self.from_hdf(file_name)
        elif file_type == self.CSV and header:
            self.from_headed_csv(file_name)
        elif file_type == self.CSV:
            self.from_csv(file_name)
        else:
            raise ValueError("Bad file: " + file_name + ". File extension must be one of csv, hdf.")
        self.init_common(file_name)

    def init_common(self, file_name):
        self.name = ntpath.basename(file_name)[:-4]
        self.variable_prefixes = get_variable_prefixes(self.variable_names)
        self.unique_variable_prefixes = set(self.variable_prefixes)
        self.predictors = numpy.nan_to_num(self.predictors)
        self.response = numpy.nan_to_num(self.response)

    def from_csv(self, csv_file):
        self.design_matrix = dm.DesignMatrix()
        self.design_matrix.from_csv(csv_file)
        self.predictors = self.design_matrix.predictors
        self.response = self.design_matrix.response
        self.num_observations, self.num_variables = self.predictors.shape
        self.variable_names = self.design_matrix.variable_names
        self.variable_type_indices = get_default_variable_type_indices(self.num_variables)
        self.variable_dict = get_simple_variable_dict(self.num_variables)

    def from_headed_csv(self, csv_file):
        self.design_matrix = dm.DesignMatrix()
        self.design_matrix.from_headed_csv(csv_file)
        self.variable_names = self.variable_names
        self.predictors = self.design_matrix.predictors
        self.num_observations, self.num_variables = self.predictors.shape
        self.response = self.design_matrix.response
        self.variable_type_indices = get_default_variable_type_indices(self.num_variables)
        self.variable_dict = get_named_variable_dict(self.variable_names, self.DEFAULT_PREFIX)

    def from_hdf(self, hdf_file):
        self.design_matrix = dm.DesignMatrix()
        self.design_matrix.from_hdf(hdf_file)
        self.predictors = self.design_matrix.predictors
        self.response = self.design_matrix.response
        self.num_observations, self.num_variables = self.predictors.shape
        days = get_hdf_days(hdf_file)
        self.variable_type_indices = get_variable_type_indices(days)
        self.variable_names = get_hdf_variable_names(days, ['lst', 'snow'])
        self.variable_dict = get_named_variable_dict(self.variable_names, self.DEFAULT_PREFIX)
        self.data_attributes['years'] = get_years_vector(hdf_file)


def get_years_vector(hdf_file):
    sd = SD(hdf_file)
    return sd.select('years').get()


def get_default_variable_type_indices(num_variables):
    return [num_variables - 1]


def get_predictors_and_response(hdf_file):
    """
    :param hdf_file:
    :return: tuple of predictors and the response
    """
    data_hdf = SD(hdf_file)
    design_matrix = data_hdf.select("design_matrix").get()
    data_hdf.end()
    return design_matrix[:, :-1], design_matrix[:, -1]


def get_hdf_days(hdf_file):
    data_hdf = SD(hdf_file)
    sds = data_hdf.select("design_matrix")
    days = []
    try:
        days.append([int(x) for x in sds.lst_days.split(",")])
    except AttributeError:
        logging.debug("No lst days available.")
    try:
        days.append([int(x) for x in sds.snow_days.split(",")])
    except AttributeError:
        logging.debug("No snow days available.")
    sds.endaccess()
    data_hdf.end()
    return days


def get_hdf_variable_names(days, name_prefixes):
    if len(days) != len(name_prefixes):
        raise ValueError("Days and prefixes must have the same length.")
    names = []
    i = 0
    for d in days:
        names.extend([str(name_prefixes[i]) + str(x) for x in d])
        i += 1
    return names


def get_named_variable_dict(names, default_prefix):
    args = [default_prefix + str(x) for x in range(0, len(names))]
    return dict(zip(args, names))


def get_variable_type_indices(days):
    indices = []
    previous = 0
    for i in days:
        current = previous + len(i)
        if len(i) != 0:
            indices.append(current - 1)
            previous = current
    return indices


def get_variable_prefixes(variable_names):
    """
    Assumes the form prefixnumber.
    :param variable_names:
    :return:
    """
    expr = re.compile('([a-zA-Z]+)')

    def get_prefix(name, expression):
        result = re.match(expression, name)
        if result:
            return result.group(1)
        return ''
    return map(partial(get_prefix, expression=expr), variable_names)


def get_simple_variable_dict(num_vars):
    args = ['ARG' + str(x) for x in range(0, num_vars)]
    simple = get_simple_variable_names(num_vars)
    return dict(zip(args, simple))
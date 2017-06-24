import ntpath

import numpy
from pyhdf.SD import SD


class LearningData:
    DEFAULT_PREFIX = 'ARG'
    CSV = "csv"

    def __init__(self):
        self.num_variables = None
        self.num_observations = None
        self.predictors = None
        self.response = None
        self.variable_names = None
        self.variable_type_indices = None
        self.variable_dict = None
        self.name = None

    def from_file(self, file_name, header=False):
        file_type = file_name[-3:]
        if file_type == "hdf":
            self.from_hdf(file_name)
        elif file_type == self.CSV and header:
            self.from_headed_csv(file_name)
        elif file_type == self.CSV:
            self.from_csv(file_name)
        else:
            raise ValueError("File extension must be one of csv, hdf.")

    def from_csv(self, csv_file):
        dat = numpy.genfromtxt(csv_file, delimiter=',', skip_header=True)
        self.predictors = dat[:, :-1]
        self.num_observations, self.num_variables = self.predictors.shape
        self.response = dat[:, -1]
        self.variable_names = get_simple_variable_names(self.num_variables)
        self.variable_type_indices = [self.num_variables - 1]
        self.variable_dict = get_simple_variable_dict(self.num_variables)
        self.name = ntpath.basename(csv_file)[:-4]

    def from_headed_csv(self, csv_file):
        dat = numpy.genfromtxt(csv_file, dtype=numpy.float, delimiter=',', names=True)
        self.variable_names = dat.dtype.names[:-1]
        dat = dat.view((dat.dtype[0], len(dat.dtype.names)))
        self.predictors = dat[:, :-1]
        self.num_observations, self.num_variables = self.predictors.shape
        self.response = dat[:, -1]
        self.variable_type_indices = [self.num_variables - 1]
        self.variable_dict = get_named_variable_dict(self.variable_names, self.DEFAULT_PREFIX)
        self.name = ntpath.basename(csv_file)[:-4]

    def from_hdf(self, hdf_file):
        self.predictors, self.response = get_predictors_and_response(hdf_file)
        self.num_observations, self.num_variables = self.predictors.shape
        days = get_hdf_days(hdf_file)
        self.variable_type_indices = get_variable_type_indices(days)
        name_prefixes = ['lst']
        if len(days) > 1:
            name_prefixes.append('snow')
        self.variable_names = get_hdf_variable_names(days, name_prefixes)
        self.variable_dict = get_named_variable_dict(self.variable_names, self.DEFAULT_PREFIX)
        self.name = ntpath.basename(hdf_file)[:-4]


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
    if sds.lst_days:
        days.append([int(x) for x in sds.lst_days.split(",")])
    if sds.snow_days:
        days.append([int(x) for x in sds.snow_days.split(",")])
    sds.endaccess()
    data_hdf.end()
    return days


def get_hdf_variable_names(days, name_prefixes):
    if len(days) != len(name_prefixes):
        raise ValueError("Must days and prefixes must have the same length.")
    names = []
    i = 0
    for d in days:
        names.extend([str(name_prefixes[i]) + str(x) for x in d])
        i += 1
    return names


def get_named_variable_dict(names, default_prefix):
    args = [default_prefix + str(x) for x in range(0, len(names))]
    return dict(zip(args, names))


def get_simple_variable_names(num_vars):
    return ['X' + str(x) for x in range(0, num_vars)]


def get_simple_variable_dict(num_vars):
    args = ['ARG' + str(x) for x in range(0, num_vars)]
    simple = get_simple_variable_names(num_vars)
    return dict(zip(args, simple))


def get_variable_type_indices(days):
    indices = []
    previous = 0
    for i in days:
        current = previous + len(i)
        if len(i) != 0:
            indices.append(current - 1)
            previous = current
    return indices

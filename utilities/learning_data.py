import ntpath

import numpy
from pyhdf.SD import SD


class LearningData:

    def __init__(self):
        self.num_variables = None
        self.num_observations = None
        self.predictors = None
        self.response = None
        self.variable_names = None
        self.variable_type_indices = None
        self.variable_dict = None
        self.name = None

    def from_file(self, file_name):
        file_type = file_name[-3:]
        if file_type == "hdf":
            self.from_hdf(file_name)
        elif file_type == "csv":
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

    def from_hdf(self, hdf_file):
        self.predictors, self.response = get_predictors_and_response(hdf_file)
        self.num_observations, self.num_variables = self.predictors.shape
        lst_days, snow_days = get_lst_and_snow_days(hdf_file)
        self.variable_type_indices = get_variable_type_indices(lst_days, snow_days)
        self.variable_names = get_hdf_variable_names(lst_days, snow_days)
        self.variable_dict = get_lst_and_snow_variable_dict(lst_days, snow_days)
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


def get_lst_and_snow_days(hdf_file):
    data_hdf = SD(hdf_file)
    sds = data_hdf.select("design_matrix")
    lst_days = [int(x) for x in sds.lst_days.split(",")]
    snow_days = [int(x) for x in sds.snow_days.split(",")]
    sds.endaccess()
    data_hdf.end()
    return lst_days, snow_days


def get_lst_names(lst_days):
    return ["lst_" + str(x) for x in lst_days]


def get_snow_names(snow_days):
    return ["snow_" + str(x) for x in snow_days]


def get_hdf_variable_names(lst_days, snow_days):
    return get_lst_names(lst_days) + get_snow_names(snow_days)


def get_lst_and_snow_variable_dict(lst_days, snow_days):
    lst_args = ["ARG" + str(x) for x in range(0, len(lst_days))]
    lst_names = get_lst_names(lst_days)
    first_args = dict(zip(lst_args, lst_names))
    snow_args = ["ARG" + str(x) for x in range(len(lst_days), len(lst_days) + len(snow_days))]
    snow_names = get_snow_names(snow_days)
    second_args = dict(zip(snow_args, snow_names))
    args = first_args.copy()
    args.update(second_args)
    return args


def get_simple_variable_names(num_vars):
    return ['X' + str(x) for x in range(0, num_vars)]


def get_simple_variable_dict(num_vars):
    args = ['ARG' + str(x) for x in range(0, num_vars)]
    simple = get_simple_variable_names(num_vars)
    return dict(zip(args, simple))


def get_variable_type_indices(lst_days, snow_days):
    return [len(lst_days) - 1, len(lst_days) + len(snow_days) - 1]

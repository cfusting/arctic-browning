from __future__ import division
import argparse
import datetime as dt
import logging

import numpy as np

import modis.modisfile as modis
from utilities import lib
from utilities import learning_data as ld

parser = argparse.ArgumentParser(description='Create design matrix.')
parser.add_argument('-l', '--lst-files', help='File containing LST file paths.', required=True)
parser.add_argument('-n', '--ndvi-files', help='File containing NDVI file paths.', required=True)
parser.add_argument('-s', '--snow-files', help='File containing SNOW file paths.')
parser.add_argument('-y', '--first-year', help='First year.', required=True, type=int)
parser.add_argument('-j', '--last-year', help='Last year.', required=True, type=int)
parser.add_argument('-t', '--t0', help='The day of the year considered t0.', required=True, type=int)
parser.add_argument('-a', '--delta', help='Number of days back from t0 to consider.', required=True, type=int)
parser.add_argument('-e', '--eta', help='Number of days from t0 back to skip.', required=True, type=int)
parser.add_argument('-v', '--verbose', help='Verbose logging.', action='store_true')
parser.add_argument('-d', '--debug', help='Debug logging.', action='store_true')
parser.add_argument('-o', '--training-out', help='Path to HDF file to save the training matrix.', required=True)
parser.add_argument('-q', '--testing-out', help='Path to HDF file to save the testing matrix.', required=True)
parser.add_argument('-m', '--missing-ratio', help='Remove variables missing at least this amount of data.', type=float)
parser.add_argument('-z', '--snow-mean', help='Remove snow variables with mean at least this large.', type=float)
parser.add_argument('-b', '--testing-year', help='Year starting testing matrix.', required=True, type=int)
args = parser.parse_args()

if args.debug:
    logging.basicConfig(level=logging.DEBUG)
elif args.verbose:
    logging.basicConfig(level=logging.INFO)


NDVI_START = 152
NDVI_END = 245
LST_LAYER = 'masked_LST_Day_1km'
SNOW_LAYER = 'upsampled_masked_Maximum_Snow_Extent'
NDVI_LAYER = 'masked_1 km monthly NDVI'


def build_matrix(modis_files, layer_name):
    """
    Extracts data from the given layer of a list of Modis files.
    :param modis_files:
    :param layer_name:
    :return: A matrix with each Modis file as a column.
    """
    columns = []
    day_of_years = []
    for fl in modis_files:
        data = fl.get_layer_data(layer_name).flatten()
        columns.append(data)
        day_of_years.append(int(fl.datetime.strftime('%j')))
        logging.debug('Added MODIS data to matrix: ' + str(fl.datetime))
        logging.debug("Possible values: " + str(np.unique(data)))
    logging.info('Matrix built for layer: ' + layer_name + '. Number of variables: ' + str(len(columns)))
    return np.vstack(columns).transpose(), day_of_years


def get_relative_datetimes(datetimes, t0, td, te):
    """
    Return a list of datetime comparable objects occurring before t0 and after t0 - td, excluding (but counting)
    t0 - te.
    :param datetimes:
    :param t0: Object comparable by datetime.
    :param td: timedelta object.
    :param te: timedelta object.
    :return: List of datetime comparable objects.
    """
    datetimes.sort(reverse=True)
    n = 0
    res = []
    for i in datetimes:
        logging.debug("Considering file: " + i.file_name)
        if t0 - td <= i.datetime <= t0:
            if i.datetime <= t0 - te:
                i.observation = n
                res.append(i)
                logging.debug("Found matching date: " + str(i.datetime) + " Period: " + str(n))
            n += 1
    return res


def getdt(yr, doy):
    return dt.datetime.strptime(str(yr) + str(doy), '%Y%j')


def get_unmasked_row_num(matrix):
    cols_masked = matrix.mask.sum(axis=1)
    return len(cols_masked[cols_masked == 0])


def get_masked_col_sums(matrix):
    return matrix.mask.sum(axis=0)


def find_means(mat, snow_mean):
    col_means = mat.mean(axis=0)
    logging.info("Column means: " + str(col_means))
    mean_indices = np.nonzero(col_means >= snow_mean)[0]
    if snow_mean and len(mean_indices) != 0:
        logging.info("Deleting columns with mean >=: " + str(snow_mean))
        logging.info(str(mean_indices))
        return mean_indices
    else:
        return []


def find_missing(mat, missing_ratio):
    missing_proportion = get_masked_col_sums(mat) / mat.shape[0]
    logging.info("Proportion missing data in columns: " + str(missing_proportion))
    missing_indices = np.nonzero(missing_proportion >= missing_ratio)[0]
    if missing_ratio and len(missing_indices) != 0:
        logging.info("Deleting columns with missing ratio >= : " + str(missing_ratio))
        logging.info(str(missing_indices))
        return missing_indices
    else:
        return []


def dynamically_remove_columns(mat, data_set, snow_mean, missing_ratio):
    indices = []
    if data_set == SNOW_LAYER:
        indices.extend(find_means(mat, snow_mean))
    indices.extend(find_missing(mat, missing_ratio))
    return indices


def get_average_day_of_year(day_of_years):
    return np.mean(np.array(day_of_years), axis=0).round().astype(int)


def build_predictor_matrix(file_paths, first_year, last_year, t0, delta, eta, data_set_name, fill_value):
    data_files = [modis.ModisFile(line.rstrip('\n')) for line in open(file_paths)]
    logging.debug("Number of HDF files: " + str(len(data_files)))
    rows = []
    day_of_year = []
    for year in range(first_year, last_year + 1):
        logging.info("Processing year: " + str(year))
        filtered = get_relative_datetimes(data_files, getdt(year, t0),
                                          dt.timedelta(days=delta), dt.timedelta(days=eta))
        mat, doys = build_matrix(filtered, data_set_name)
        rows.append(mat)
        day_of_year.append(doys)
    matrix = np.vstack(rows)
    logging.debug(str(day_of_year))
    average_day_of_year = get_average_day_of_year(day_of_year)
    logging.info("Average day of year: " + str(average_day_of_year))
    masked_matrix = np.ma.masked_equal(matrix, fill_value)
    logging.info("Predictor matrix built with unique values: " + str(np.unique(matrix)))
    available_rows = get_unmasked_row_num(masked_matrix)
    row_num = masked_matrix.shape[0]
    logging.info("Proportion of rows without missing values: " + str(available_rows / row_num))
    average_day_of_year_cleaned = average_day_of_year
    indices_to_delete = dynamically_remove_columns(masked_matrix, data_set_name, args.snow_mean, args.missing_ratio)
    if len(indices_to_delete) != 0:
        indices_to_delete = np.unique(indices_to_delete)
        average_day_of_year_cleaned = [el for i, el in enumerate(average_day_of_year) if i not in indices_to_delete]
        logging.info("Deleting columns: " + str(indices_to_delete))
        cleaned_matrix = np.delete(masked_matrix, indices_to_delete, axis=1)
        masked_matrix = np.ma.masked_equal(cleaned_matrix, fill_value)
        new_available_rows = get_unmasked_row_num(masked_matrix)
        logging.info("New proportion of rows without missing values: " + str(new_available_rows / row_num))
        logging.info("Built cleaned predictor matrix with shape: " + str(masked_matrix.shape))
    return masked_matrix, average_day_of_year_cleaned


def build_ndvi_matrix(file_paths, first_year, last_year, ndvi_start, ndvi_end):
    ndvi_files = [modis.ModisFile(line.rstrip('\n')) for line in open(file_paths)]
    ndvi_rows = []
    for year in range(first_year, last_year + 1):
        ndvi_filtered = filter(lambda x: getdt(year, ndvi_start) <= x.datetime <= getdt(year, ndvi_end), ndvi_files)
        mat, ndvi_days = build_matrix(ndvi_filtered, NDVI_LAYER)
        ndvi_rows.append(mat)
    ndvi_stack = np.vstack(ndvi_rows)
    ndvi_masked = np.ma.masked_equal(ndvi_stack, lib.NDVI_NO_DATA)
    ndvi_vector = ndvi_masked.mean(axis=1)
    logging.info('NDVI matrix constructed. Shape: ' + str(ndvi_vector.shape))
    rows = ndvi_vector.shape[0]
    return ndvi_vector.reshape(rows, 1), []


def build_years_vector(years, total_observations):
    observations = total_observations / len(years)
    return np.hstack([np.full(observations, year) for year in years])


def build_design_matrix(years, matrices):
    matrix_list = list(matrices)
    years_column = build_years_vector(years, matrix_list[0].shape[0])
    matrix_list.append(years_column.reshape((years_column.shape[0], 1)))
    design_masked = np.ma.concatenate(matrix_list, axis=1)
    logging.info("Removing rows with missing values.")
    dm = np.ma.compress_rows(design_masked)
    return dm


def get_hdf_attributes():
    return {'training_first_year': args.first_year,
            'testing_first_year': args.testing_year,
            'testing_last_year': args.last_year,
            't0': args.t0,
            'delta': args.delta,
            'eta': args.eta,
            'missing_ratio': args.missing_ratio,
            'snow_mean': args.snow_mean}


def build_hdf(file_name, matrix, years, names):
    learning_data = ld.LearningData()
    learning_data.from_data(matrix, names, 'none')
    learning_data.meta_layers['years'] = years
    learning_data.attributes = get_hdf_attributes()
    learning_data.to_hdf(file_name)


def split_data(matrix, testing_year):
    logging.info("Raw matrix shape: " + str(matrix.shape))
    training = matrix[matrix[:, -1] < testing_year][:, :-1]
    testing = matrix[matrix[:, -1] >= testing_year][:, :-1]
    logging.info("Training data shape: " + str(training.shape))
    logging.info("Testing data shape: " + str(testing.shape))
    return training, testing, matrix[:, -1]


def build_variable_names(days_list, snow):
    names = ['lst' + str(d) for d in days_list[0]]
    if snow:
        names.extend(['snow' + str(d) for d in days_list[1]])
    return names


matrices_days = [build_predictor_matrix(args.lst_files, args.first_year, args.last_year, args.t0,
                                        args.delta, args.eta, LST_LAYER, lib.LST_NO_DATA)]
if args.snow_files:
    matrices_days.append(build_predictor_matrix(args.snow_files, args.first_year, args.last_year, args.t0,
                                                args.delta, args.eta, SNOW_LAYER, lib.FILL_SNOW))
matrices_days.append(build_ndvi_matrix(args.ndvi_files, args.first_year, args.last_year, NDVI_START, NDVI_END))
mats, days = zip(*matrices_days)
variable_names = build_variable_names(days, args.snow_files)
raw_matrix = build_design_matrix(range(args.first_year, args.last_year + 1), mats)
training_matrix, testing_matrix, years_vector = split_data(raw_matrix, args.testing_year)
build_hdf(args.training_out, training_matrix, years_vector, variable_names)
build_hdf(args.testing_out, testing_matrix, years_vector, variable_names)

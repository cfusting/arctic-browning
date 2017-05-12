import argparse
import datetime as dt
import logging

import numpy as np
from pyhdf.SD import SD, SDC

import modis.modisfile as modis

parser = argparse.ArgumentParser(description='Create design matrix.')
parser.add_argument('-l', '--lst-files', help='File containing LST file paths.', required=True)
parser.add_argument('-n', '--ndvi-files', help='File containing NDVI file paths.', required=True)
parser.add_argument('-s', '--snow-files', help='File containing SNOW file paths.', required=True)
parser.add_argument('-y', '--first-year', help='First year.', required=True, type=int)
parser.add_argument('-j', '--last-year', help='Last year.', required=True, type=int)
parser.add_argument('-t', '--t0', help='The day of the year considered t0.', required=True, type=int)
parser.add_argument('-a', '--delta', help='Number of days back from t0 to consider.', required=True, type=int)
parser.add_argument('-e', '--eta', help='Number of days from t0 back to skip.', required=True, type=int)
parser.add_argument('-v', '--verbose', help='Verbose logging.', action='store_true')
parser.add_argument('-d', '--debug', help='Debug logging.', action='store_true')
parser.add_argument('-o', '--out-file', help='Name of HDF file to save the design matrix.', required=True)
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
LST_NO_DATA = 0
NDVI_NO_DATA = -3000
SNOW_NO_DATA = 255


def build_matrix(modis_files, layer_name):
    """
    Extracts data from the given layer of a list of Modis files.
    :param modis_files:
    :param layer_name:
    :return: A matrix with each Modis file as a column.
    """
    columns = []
    for fl in modis_files:
        columns.append(fl.get_layer_data(layer_name).flatten())
        logging.info('Added MODIS data to matrix: ' + str(fl.datetime))
    logging.info('Matrix built for layer: ' + layer_name + '. Number of variables: ' + str(len(columns)))
    return np.vstack(columns).transpose()


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


def build_predictor_matrix(file_paths, first_year, last_year, t0, delta, eta, data_set_name, fill_value):
    data_files = [modis.ModisFile(line.rstrip('\n')) for line in open(file_paths)]
    logging.debug("Number of LST files: " + str(len(data_files)))
    rows = []
    for year in range(first_year, last_year + 1):
        logging.info("Processing year: " + str(year))
        filtered = get_relative_datetimes(data_files, getdt(year, t0),
                                          dt.timedelta(days=delta), dt.timedelta(days=eta))
        rows.append(build_matrix(filtered, data_set_name))
    matrix = np.vstack(rows)
    masked_matrix = np.ma.masked_equal(matrix, fill_value)
    return masked_matrix


def build_ndvi_matrix(file_paths, first_year, last_year, ndvi_start, ndvi_end):
    ndvi_files = [modis.ModisFile(line.rstrip('\n')) for line in open(file_paths)]
    ndvi_rows = []
    for year in range(first_year, last_year + 1):
        ndvi_filtered = filter(lambda x: getdt(year, ndvi_start) <= x.datetime <= getdt(year, ndvi_end), ndvi_files)
        ndvi_rows.append(build_matrix(ndvi_filtered, NDVI_LAYER))
    ndvi_stack = np.vstack(ndvi_rows)
    ndvi_masked = np.ma.masked_equal(ndvi_stack, NDVI_NO_DATA)
    ndvi_vector = ndvi_masked.mean(axis=1)
    logging.info('NDVI matrix constructed. Shape: ' + str(ndvi_vector.shape))
    rows = ndvi_vector.shape[0]
    return ndvi_vector.reshape(rows, 1)


def build_design_matrix(*matrices):
    design_masked = np.ma.concatenate(matrices, axis=1)
    dm = np.ma.compress_rows(design_masked)
    logging.info("Design Matrix shape: " + str(dm.shape))
    logging.debug(str(dm))
    return dm

lst_matrix = build_predictor_matrix(args.lst_files, args.first_year, args.last_year, args.t0, args.delta, args.eta,
                                    LST_LAYER, LST_NO_DATA)
snow_matrix = build_predictor_matrix(args.snow_files, args.first_year, args.last_year, args.t0, args.delta, args.eta,
                                     SNOW_LAYER, SNOW_NO_DATA)
ndvi_matrix = build_ndvi_matrix(args.ndvi_files, args.first_year, args.last_year, NDVI_START, NDVI_END)
design_matrix = build_design_matrix(lst_matrix, snow_matrix, ndvi_matrix)
sd = SD(args.out_file, SDC.WRITE | SDC.CREATE)
sds = sd.create("design_matrix", SDC.FLOAT64, design_matrix.shape)
sds.first_year = args.first_year
sds.last_year = args.last_year
sds.t0 = args.t0
sds.delta = args.delta
sds.eta = args.eta
sds[:] = design_matrix
sds.endaccess()
sd.end()

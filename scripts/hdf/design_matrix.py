import argparse
import datetime as dt
import logging

import numpy as np
from pyhdf.SD import SD, SDC

import modis.modisfile as modis

parser = argparse.ArgumentParser(description='Create design matrix.')
parser.add_argument('-l', '--lst-files', help='File containing LST file paths.', required=True)
parser.add_argument('-n', '--ndvi-files', help='File containing NDVI file paths.', required=True)
parser.add_argument('-y', '--first-year', help='First year.', required=True, type=int)
parser.add_argument('-j', '--last-year', help='Last year.', required=True, type=int)
parser.add_argument('-t', '--t0', help='The day of the year considered t0.', required=True, type=int)
parser.add_argument('-d', '--delta', help='Number of days back from t0 to consider.', required=True, type=int)
parser.add_argument('-e', '--eta', help='Number of days from t0 back to skip.', required=True, type=int)
parser.add_argument('-v', '--verbose', help='Verbose.', action='store_true')
parser.add_argument('-o', '--out-file', help='Name of HDF file to save the design matrix.', required=True)
args = parser.parse_args()

if args.verbose:
    logging.basicConfig(level=logging.DEBUG)

NDVI_START = 152
NDVI_END = 245


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
        logging.debug('Added MODIS data to matrix: ' + str(fl.datetime))
    logging.debug('Matrix built for layer: ' + layer_name + '. Number of variables: ' + str(len(columns)))
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

lst_files = [modis.ModisFile(line.rstrip('\n')) for line in open(args.lst_files)]
logging.debug("Number of LST files: " + str(len(lst_files)))
lst_rows = []
for year in range(args.first_year, args.last_year + 1):
    logging.debug("Processing year: " + str(year))
    lst_filtered = get_relative_datetimes(lst_files, getdt(year, args.t0),
                                          dt.timedelta(days=args.delta), dt.timedelta(days=args.eta))
    lst_rows.append(build_matrix(lst_filtered, 'masked_LST_Day_1km'))
lst_matrix = np.vstack(lst_rows)
lst_masked = np.ma.masked_equal(lst_matrix, 0)
logging.debug('LST matrix constructed. Shape: ' + str(lst_masked.shape))
ndvi_files = [modis.ModisFile(line.rstrip('\n')) for line in open(args.ndvi_files)]
ndvi_rows = []
for year in range(args.first_year, args.last_year + 1):
    ndvi_filtered = filter(lambda x: getdt(year, NDVI_START) <= x.datetime <= getdt(year, NDVI_END), ndvi_files)
    ndvi_rows.append(build_matrix(ndvi_filtered, "masked_1 km monthly NDVI"))
ndvi_matrix = np.vstack(ndvi_rows)
ndvi_masked = np.ma.masked_equal(ndvi_matrix, -3000)
ndvi_vector = ndvi_masked.mean(axis=1)
logging.debug('NDVI matrix constructed. Shape: ' + str(ndvi_vector.shape))
rows = ndvi_vector.shape[0]
ndvi_transpose = ndvi_vector.reshape(rows, 1)
design_masked = np.ma.concatenate([lst_matrix, ndvi_transpose], axis=1)
design_matrix = np.ma.compress_rows(design_masked)
logging.debug("Design Matrix shape: " + str(design_matrix.shape))
logging.debug(str(design_matrix))
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

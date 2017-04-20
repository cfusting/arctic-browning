from pyhdf.SD import SD, SDC
import argparse
from lib import build_lst_mask, build_ndvi_mask, logging, build_snow_mask
import numpy as np
import sys

NDVI = 'ndvi'
LST = 'lst'
SNOW = 'snow'

parser = argparse.ArgumentParser(description='Add mask and masked data to a MODIS hdf file.')
parser.add_argument('-i', '--in-file', help='Name of the file containing a list of hdf files to process.',
                    required=True)
parser.add_argument('-b', '--band', help='Name of the band containing the data to be masked.', required=True)
parser.add_argument('-q', '--quality', help='Name of the quality control band.')
parser.add_argument('-o', '--overwrite', help='Overwrite masked data.', action='store_true')
parser.add_argument('-t', '--type', help='Data Type.', choices=[LST, NDVI, SNOW], required=True)
parser.add_argument('-v', '--verbose', help='Verbose.', action='store_true')
args = parser.parse_args()

if args.verbose:
    logging.basicConfig(level=logging.DEBUG)

LST_NUMPY = np.uint16
LST_SDC = SDC.UINT16
NDVI_NUMPY = np.int16
NDVI_SDC = SDC.INT16
SNOW_NUMPY = np.int8
SNOW_SDC = SDC.INT8
DAT_NUMPY = None
DAT_SDC = None

if args.type == LST:
    DAT_NUMPY = LST_NUMPY
    DAT_SDC = LST_SDC
elif args.type == NDVI:
    DAT_NUMPY = NDVI_NUMPY
    DAT_SDC = NDVI_SDC
elif args.type == SNOW:
    DAT_NUMPY = SNOW_NUMPY
    DAT_SDC = SNOW_SDC

file_list = [line.rstrip('\n') for line in open(args.in_file)]
for fl in file_list:
    sd = SD(fl, SDC.WRITE | SDC.CREATE)
    dat = sd.select(args.band)
    if args.quality:
        quality = sd.select(args.quality)
    shp = dat.get().shape
    MASKED_DAT_NAME = "masked_" + args.band
    if MASKED_DAT_NAME in sd.datasets() and not args.overwrite:
        print MASKED_DAT_NAME
        print sd.datasets()
        sys.exit('Masked data present. Exiting.')
    sds_data = None
    if MASKED_DAT_NAME not in sd.datasets():
        sds_data = sd.create(MASKED_DAT_NAME, DAT_SDC, shp)
    else:
        sds_data = sd.select(MASKED_DAT_NAME)
    fill_value = dat.getfillvalue()
    sds_data.setfillvalue(fill_value)
    mask = None
    if args.type == LST:
        mask = build_lst_mask(dat.get(), quality.get())
        masked_dat = np.ma.array(dat.get(), mask=mask, fill_value=fill_value, dtype=DAT_NUMPY)
    elif args.type == NDVI:
        mask = build_ndvi_mask(dat.get(), quality.get())
        masked_dat = np.ma.array(dat.get(), mask=mask, fill_value=fill_value, dtype=DAT_NUMPY)
    elif args.type == SNOW:
        mask = build_snow_mask(dat.get())
        masked_dat = np.ma.array(dat.get(), mask=mask, fill_value=fill_value, dtype=DAT_NUMPY)
    sds_data[:] = masked_dat.filled()
    logging.debug('Written values: ' + str(sds_data.get()))
    sds_data.endaccess()
    sd.end()

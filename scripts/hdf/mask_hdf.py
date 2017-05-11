import argparse
import logging
import numpy as np
from pyhdf.SD import SD, SDC

from utilities import lib

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

LST_SDC = SDC.UINT16
NDVI_SDC = SDC.INT16
SNOW_SDC = SDC.UINT8
DAT_SDC = None

if args.type == LST:
    DAT_SDC = LST_SDC
elif args.type == NDVI:
    DAT_SDC = NDVI_SDC
elif args.type == SNOW:
    DAT_SDC = SNOW_SDC

file_list = [line.rstrip('\n') for line in open(args.in_file)]
for fl in file_list:
    sd = SD(fl, SDC.WRITE | SDC.CREATE)
    dat = sd.select(args.band)
    if args.quality:
        quality = sd.select(args.quality)
    MASKED_DAT_NAME = "masked_" + args.band
    if MASKED_DAT_NAME in sd.datasets() and not args.overwrite:
        logging.info("Masked data present, skipping:")
        logging.debug(MASKED_DAT_NAME)
        logging.debug(sd.datasets())
        sd.end()
    else:
        sds_data = None
        sds_data = sd.create(MASKED_DAT_NAME, DAT_SDC, dat.get().shape)
        fill_value = dat.getfillvalue()
        sds_data.setfillvalue(fill_value)
        mask = None
        data = None
        if args.type == LST:
            mask = lib.build_lst_mask(dat.get(), quality.get())
            data = dat.get()
        elif args.type == NDVI:
            mask = lib.build_ndvi_mask(dat.get(), quality.get())
            data = dat.get()
        elif args.type == SNOW:
            mask = lib.build_snow_mask(dat.get())
            data = dat.get()
        masked_dat = np.ma.array(data, mask=mask, fill_value=fill_value, dtype=dat.get().dtype)
        sds_data[:] = masked_dat.filled()
        logging.debug('Written values: ' + str(sds_data.get()))
        sds_data.endaccess()
        sd.end()

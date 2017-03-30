from pyhdf.SD import SD, SDC
import argparse
from lib import build_lst_mask, logging
import numpy as np
import sys


parser = argparse.ArgumentParser(description='Add mask and masked data to a MODIS hdf file.')
parser.add_argument('-i', '--in-file', help='Name of the file containing a list of hdf files to process.',
                    required=True)
parser.add_argument('-b', '--band', help='Name of the band containing the data to be masked.', required=True)
parser.add_argument('-q', '--quality', help='Name of the quality control band.', required=True)
parser.add_argument('-o', '--overwrite', help='Overwrite masked data.', action='store_true')
args = parser.parse_args()

logging.basicConfig(level=logging.DEBUG)

file_list = [line.rstrip('\n') for line in open(args.in_file)]
for fl in file_list:
    sd = SD(fl, SDC.WRITE | SDC.CREATE)
    dat = sd.select(args.band)
    quality = sd.select(args.quality)
    shp = dat.get().shape
    MASKED_DAT_NAME = "masked_" + args.band
    if MASKED_DAT_NAME in sd.datasets() and not args.overwrite:
        sys.exit('Masked data present. Exiting.')
    sds_data = None
    if MASKED_DAT_NAME not in sd.datasets():
        sds_data = sd.create(MASKED_DAT_NAME, SDC.UINT16, shp)
    else:
        sds_data = sd.select(MASKED_DAT_NAME)
    fill_value = dat.getfillvalue()
    sds_data.setfillvalue(fill_value)
    mask = build_lst_mask(dat.get(), quality.get())
    masked_dat = np.ma.array(dat.get(), mask=mask, fill_value=fill_value, dtype=np.uint16)
    sds_data[:] = masked_dat.filled()
    logging.debug('Written values: ' + str(sds_data.get()))
    sds_data.endaccess()
    sd.end()

import argparse
import logging
import numpy as np
from pyhdf.SD import SD, SDC

from utilities import lib

parser = argparse.ArgumentParser(description='Add mask and masked data to a MODIS hdf file.')
parser.add_argument('-i', '--in-file', help='Name of the file containing a list of hdf files to process.',
                    required=True)
parser.add_argument('-v', '--verbose', help='Verbose.', action='store_true')
args = parser.parse_args()

SNOW_LAYER = 'masked_Maximum_Snow_Extent'
SNOW_SDC = SDC.UINT8

if args.verbose:
    logging.basicConfig(level=logging.DEBUG)

file_list = [line.rstrip('\n') for line in open(args.in_file)]
for fl in file_list:
    sd = SD(fl, SDC.CREATE | SDC.WRITE)
    snow = sd.select(SNOW_LAYER)
    masked_snow = np.ma.masked_equal(snow, snow.getfillvalue())
    masked_snow._sharedmask = False
    lib.convert_snow_to_binary(masked_snow)
    data = lib.upsample_snow(masked_snow, lib.masked_binary_logic)
    logging.debug("Snow shape: " + str(data.shape))
    logging.debug("Snow data: " + str(data))
    sds_data = sd.create("upsampled" + SNOW_LAYER, SNOW_SDC, (1200, 1200))
    logging.info("Writing upsampled data from: " + fl)
    sds_data[:] = masked_snow.filled()
    sds_data.endaccess()
    sd.end()

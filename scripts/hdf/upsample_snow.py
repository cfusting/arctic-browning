import argparse
import logging
import numpy as np
from pyhdf.SD import SD, SDC

from utilities import lib

parser = argparse.ArgumentParser(description='Add mask and masked data to a MODIS hdf file.')
parser.add_argument('-f', '--file', help='Path to the snow hdf with mask layer.', required=True)
parser.add_argument('-l', '--layer', help='Masked layer name.', required=True)
parser.add_argument('-v', '--verbose', help='Verbose logging.', action='store_true')
parser.add_argument('-d', '--debug', help='Debug logging.', action='store_true')
args = parser.parse_args()

SNOW_LAYER = args.layer
SNOW_SDC = SDC.UINT8

if args.debug:
    logging.basicConfig(level=logging.DEBUG)
elif args.verbose:
    logging.basicConfig(level=logging.INFO)

sd = SD(args.file, SDC.CREATE | SDC.WRITE)
snow = sd.select(args.layer)
masked_snow = np.ma.masked_equal(snow.get(), snow.getfillvalue())
masked_snow._sharedmask = False
lib.convert_snow_to_binary(masked_snow)
data = lib.upsample_snow(masked_snow, lib.masked_binary_logic)
logging.debug("Snow shape: " + str(data.shape))
logging.debug("Snow data: " + str(data))
sds_data = sd.create("upsampled_" + args.layer, SNOW_SDC, (1200, 1200))
logging.info("Writing upsampled data from: " + args.file)
sds_data[:] = data.filled()
sds_data.endaccess()
sd.end()

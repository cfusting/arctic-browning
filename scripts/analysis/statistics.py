import argparse

import gdal
import numpy as np
import numpy.ma as ma

from utilities import lib

parser = argparse.ArgumentParser(description='Fetch statistics from a raster.')
parser.add_argument('-i', '--input', help='Input raster', required=True)
parser.add_argument('-r', '--reliability', help='Pixel reliability raster', required=True)
parser.add_argument('-k', '--key', help='Unique Key', required=True)
args = parser.parse_args()

inputraster = gdal.Open(args.input)
reliabilityraster = gdal.Open(args.reliability)
inputband = inputraster.GetRasterBand(1)
reliabilityband = reliabilityraster.GetRasterBand(1)
inputarray = np.array(inputband.ReadAsArray(), np.int16)
reliabilityarray = np.array(reliabilityband.ReadAsArray(), np.int8)
lib.build_qa_mask(inputarray, reliabilityarray)
masked = ma.array(inputarray, mask=reliabilityarray)

pixels = inputarray.size - reliabilityarray.sum()
mean = masked.mean()
stdv = masked.std()
min = masked.min()
max = masked.max()

print str(args.key) + "," + str(pixels) + "," + str(mean) + "," + str(stdv) + "," + str(min) + "," + str(max)


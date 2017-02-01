import argparse
import numpy as np
import gdal
from gdalconst import *
from osgeo import osr


# Function to read the original file's projection:
def get_geo_info(srcds):
    ndv = srcds.GetRasterBand(1).GetNoDataValue()
    xsize = srcds.RasterXSize
    ysize = srcds.RasterYSize
    geot = srcds.GetGeoTransform()
    projection = osr.SpatialReference()
    projection.ImportFromWkt(srcds.GetProjectionRef())
    datatype = srcds.GetRasterBand(1).DataType
    return ndv, xsize, ysize, geot, projection, datatype


# Function to write a new file.
def create_geotiff(name, array, driver, ndv, nde,
                   xsize, ysize, geot, projection, datatype):
    newfilename = name + '.tif'
    # Set nans to the original No Data Value
    array[array == nde] = ndv
    # Set up the dataset
    dataset = driver.Create(newfilename, xsize, ysize, 1, datatype)
    # the '1' is for band 1.
    dataset.SetGeoTransform(geot)
    dataset.SetProjection(projection.ExportToWkt())
    # Write the array
    dataset.GetRasterBand(1).WriteArray(array)
    dataset.GetRasterBand(1).SetNoDataValue(ndv)
    return newfilename


def main(filename, output):
    driver = gdal.GetDriverByName("GTiff")
    srcds = gdal.Open(filename)
    band = srcds.GetRasterBand(1)
    array = band.ReadAsArray()
    newarray = array + 20
    ndv, xsize, ysize, geot, projection, datatype = get_geo_info(srcds)
    create_geotiff(output, newarray, driver, ndv, -3000, xsize, ysize, geot, projection, datatype)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Test to ensure these functions work.')
    parser.add_argument('-i', '--input', help='input file', required=True)
    parser.add_argument('-o', '--output', help='output file', required=True)
    args = parser.parse_args()
    main(args.input, args.output)


#!/bin/bash
if [ "$1" = "" ]; then
	echo usage: $0 filelist
	exit
fi
id=$(grep -oh -m 1 "A[0-9]*[0-9]" $1)
modis_mosaic.py -s "1 1 1 0 0 0 0 0 0 0 0 1" -v -o mosaic $1
declare -a dattype=("NDVI" "EVI" "VI Quality" "pixel reliability")
for d in "${dattype[@]}"
do
    echo $d

    # Reproject
    modis_convert.py -v -s "( 1 )" -o "mosaics/"$id"_mosaic_250m 16 days $d" -e 4326 $id"_mosaic_250m 16 days $d"".vrt"

    # Extract the EVI from the mosaic.
    #gdal_translate -ot Int16 -b 1 -projwin 5 71.5 25.66667 66.56289 -projwin_srs EPSG:4326 "mosaics/"$id"_mosaic_250m 16 days $d"".tif" "mosaics/"$id"_clipped_mosaic_250m 16 days $d"".tif"
done

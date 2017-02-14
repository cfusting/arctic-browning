#!/bin/bash
if [ "$1" = "" ]; then
	echo usage: $0 filelist
	exit
fi
id=$(grep -oh -m 1 "A[0-9]*[0-9]" $1)
modis_mosaic.py -s "1 1 0 0 1 1 0 0 0 0 0 0" -v -o mosaic $1
declare -a dattype=("LST_Day_1km" "QC_Day" "LST_Night_1km" "QC_Night")
for d in "${dattype[@]}"
do
    echo "Processing: "$d
    # Reproject
    modis_convert.py -v -s "( 1 )" -o "mosaics/"$id"_mosaic_250m 16 days $d" -e 4326 $id"_mosaic_250m 16 days $d"".vrt"
done
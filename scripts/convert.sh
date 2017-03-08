#!/bin/bash
if [ "$1" = "" ]; then
	echo usage: $0 filelist
	exit
fi
id=$(grep -oh -m 1 "\.A[0-9]*[0-9]\." $1 | sed 's/\.//g')
modis_mosaic.py -s "1 1 1 0 0 0 0 0 0 0 0 0" -v -o mosaic $1
declare -a dattype=("NDVI" "EVI" "VI Quality")
for d in "${dattype[@]}"
do
    outfile="mosaics/"$id"_mosaic_1_km_monthly_"$d
    vrtfile=$id"_mosaic_1 km monthly "$d".vrt"
    echo "Processing: $vrtfile and putting results in $outfile"
    modis_convert.py -v -s "( 1 )" -o "${outfile}" -e 4326 "${vrtfile}"
done

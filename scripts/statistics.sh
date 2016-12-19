#!/bin/bash
source $HOME"/.bash_profile"
source $HOME"/modis/bin/activate"
# Each date has a unique id
ids=$(ls $HOME"/ndvi_terra/mosaics" | grep -oh A[0-9]*[0-9] | uniq)
NDVIOUT=$HOME"/browning/results/ndvistats.csv"
EVIOUT=$HOME"/browning/results/evistats.csv"
echo "key,pixels,mean,std,min,max" > $NDVIOUT
echo "key,pixels,mean,std,min,max" > $EVIOUT
for i in $ids; do
        SCRIPT=$HOME"/browning/scripts/statistics.py"
        NDVI=$HOME"/ndvi_terra/mosaics/"$i"_mosaic_250m 16 days NDVI.tif" 
        EVI=$HOME"/ndvi_terra/mosaics/"$i"_mosaic_250m 16 days EVI.tif" 
        RELIABILITY=$HOME"/ndvi_terra/mosaics/"$i"_mosaic_250m 16 days pixel reliability.tif"
        python $SCRIPT -i "$NDVI" -r "$RELIABILITY" -k $i >> $NDVIOUT
        python $SCRIPT -i "$EVI" -r "$RELIABILITY" -k $i >> $EVIOUT
done
deactivate

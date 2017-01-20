#!/bin/bash
source $HOME"/.bash_profile"
source $HOME"/modis/bin/activate"
SCRIPT=$HOME"/arctic-browning/scripts/temporal_statistics.py"
NDVIOUT=$HOME"/results/ndvi_temporal_stats.csv"
DIRECTORY=$HOME"/ndvi_terra/mosaics"
echo "mean,sd,min,max" > $NDVIOUT
python $SCRIPT -s 2000 -e 2016 -f 162 -l 255 -d $DIRECTORY -k 'clipped_mosaic.*NDVI' -r 'clipped_mosaic.*reliability' -j '\d{7}' >> $NDVIOUT

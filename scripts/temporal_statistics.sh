#!/bin/bash
source $HOME"/.bash_profile"
source $HOME"/modis/bin/activate"
SCRIPT=$HOME"/arctic-browning/scripts/temporal_statistics.py"
NDVIOUT=$HOME"/results/ndvi_temporal_stats.csv"
DIRECTORY=$HOME"/v5_ndvi_terra/mosaics"
echo "year,mean,sd,min,max" > $NDVIOUT
python $SCRIPT -s 2000 -e 2016 -f 161 -l 232 -d $DIRECTORY -k 'clipped_mosaic.*NDVI' -r 'clipped_mosaic.*reliability' -j '\d{7}' -v -b $HOME/job_logs/temporal_stats.log >> $NDVIOUT

#!/bin/bash
source $HOME"/.bash_profile"
source $HOME"/geospatial/bin/activate"
SCRIPT=$HOME"/arctic-browning/scripts/temporal_statistics.py"
DIRECTORY=$HOME"/scratch/ndvi_monthly/mosaics/${year}"
NDVIOUT=$DIRECTORY"/${year}.csv"
echo "year,tindvi,weight" > $NDVIOUT
python $SCRIPT -s ${year} -e ${year} -f 161 -l 232 -d $DIRECTORY -k '.*NDVI.*' -r '.*Quality.*' -j '\d{7}' -v -n -b $HOME/job_logs/temporal_stats.log > $NDVIOUT
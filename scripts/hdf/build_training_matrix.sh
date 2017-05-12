#!/bin/bash
python $HOME"/arctic-browning/scripts/hdf/design_matrix.py" \
-l $HOME"/modis_data/lst_8day_1km/hdfs.list" \
-n $HOME"/modis_data/ndvi_monthly_1km/hdfs.list" \
-s $HOME"/modis_data/snow_8day_500m/hdfs.list" \
-y 2011 -j 2014 -t 255 -a 365 -e 0 -o $HOME"/design_matrices/training_matrix.hdf" -v
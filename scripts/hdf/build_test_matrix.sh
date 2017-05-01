#!/bin/bash
python $HOME"/arctic-browning/scripts/hdf/design_matrix.py" \
-l $HOME"/modis_data/lst_8day_1km/hdfs.list" \
-n $HOME"/modis_data/ndvi_monthly_1km/hdfs.list" \
-y 2015 -j 2016 -t 255 -d 365 -e 0 -o $HOME"/design_matrices/test_matrix.hdf" -v
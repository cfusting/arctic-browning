#!/bin/bash
#PBS -l nodes=1:ppn=1,pmem=32gb,pvmem=32gb
#PBS -l walltime=01:00:00
#PBS -N test_matrix
#PBS -o /users/c/f/cfusting/job_logs
#PBS -e /users/c/f/cfusting/job_logs
#PBS -q shortq
source ~/.bash_profile
cd ~/modis_data/lst_8day_1km
find `pwd` -name "*hdf" > hdfs.list
cd ~/modis_data/ndvi_monthly_1km
find `pwd` -name "*hdf" > hdfs.list
export PYTHONPATH=$HOME/gp_mecl:$HOME/arctic-browning
python $ARCTIC_HOME/scripts/hdf/design_matrix.py \
-l $MODIS_DATA_HOME"/lst_8day_1km/hdfs.list" \
-n $MODIS_DATA_HOME"/ndvi_monthly_1km/hdfs.list" \
-s $MODIS_DATA_HOME"/snow_8day_500m/hdfs.list" \
-y 2015 -j 2016 -t 255 -a 365 -e 0 -o $ARCTIC_DATA_HOME/design_matrices/test_matrix.hdf -v \
-r 40 44 -x 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 43 44

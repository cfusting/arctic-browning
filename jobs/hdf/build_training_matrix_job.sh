#!/bin/bash
#PBS -l nodes=1:ppn=1,pmem=32gb,pvmem=32gb
#PBS -l walltime=03:00:00
#PBS -N training_matrix
#PBS -o /users/c/f/cfusting/job_logs
#PBS -e /users/c/f/cfusting/job_logs
#PBS -q shortq
cd ~/modis_data/lst_8day_1km
find `pwd` -name "*hdf" > hdfs.list
cd ~/modis_data/ndvi_monthly_1km
find `pwd` -name "*hdf" > hdfs.list
cd ~/modis_data/snow_8day_500m
find `pwd` -name "*hdf" > hdfs.list
export PYTHONPATH=$HOME/gp_mecl:$HOME/arctic-browning
python $HOME"/arctic-browning/scripts/hdf/design_matrix.py" \
-l $HOME"/modis_data/lst_8day_1km/hdfs.list" \
-n $HOME"/modis_data/ndvi_monthly_1km/hdfs.list" \
-s $HOME"/modis_data/snow_8day_500m/hdfs.list" \
-y 2011 -j 2014 -t 255 -a 365 -e 0 -o $HOME"/design_matrices/training_matrix.hdf" -v

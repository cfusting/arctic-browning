#!/bin/bash
#PBS -l nodes=1:ppn=1,pmem=32gb,pvmem=32gb
#PBS -l walltime=01:00:00
#PBS -N test_matrix
#PBS -o /users/c/f/cfusting/job_logs
#PBS -e /users/c/f/cfusting/job_logs
#PBS -q shortq
cd ~/modis_data/lst_8day_1km
find `pwd` -name "*hdf" > hdfs.list
cd ~/modis_data/ndvi_monthly_1km
find `pwd` -name "*hdf" > hdfs.list
source $HOME/arctic-browning/scripts/hdf/build_test_matrix.sh
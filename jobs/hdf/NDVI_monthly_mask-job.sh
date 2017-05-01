#!/bin/bash
#PBS -l nodes=1:ppn=1
#PBS -l walltime=03:00:00
#PBS -N ndvi_mask
#PBS -o /users/c/f/cfusting/job_logs
#PBS -e /users/c/f/cfusting/job_logs
#PBS -q shortq
cd ~/modis_data/lst_8day_1km
find `pwd` -name "*hdf" > hdfs.list
cd ~/modis_data/ndvi_monthly_1km
find `pwd` -name "*hdf" > hdfs.list
python ~/arctic-browning/scripts/mask_hdf.py -i hdfs.list -b '1 km monthly NDVI' -q '1 km monthly VI Quality' -t ndvi -v -o

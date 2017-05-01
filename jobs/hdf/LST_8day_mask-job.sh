#!/bin/bash
#PBS -l nodes=1:ppn=1
#PBS -l walltime=03:00:00
#PBS -N lst_mask
#PBS -o /users/c/f/cfusting/job_logs
#PBS -e /users/c/f/cfusting/job_logs
#PBS -q shortq
cd ~/modis_data/lst_8day_1km
find `pwd` -name "*hdf" > hdfs.list
cd ~/modis_data/ndvi_monthly_1km
find `pwd` -name "*hdf" > hdfs.list
python ~/arctic-browning/scripts/hdf/mask_hdf.py -i hdfs.list -b LST_Day_1km -q QC_Day -t lst -v -o

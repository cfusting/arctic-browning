#!/bin/bash
#PBS -l nodes=1:ppn=1
#PBS -l walltime=03:00:00
#PBS -N hdfmask
#PBS -o /users/c/f/cfusting/job_logs
#PBS -e /users/c/f/cfusting/job_logs
#PBS -q shortq
cd ~/scratch/ndvi_monthly
ls | egrep "*.hdf$" > ndvi.list
python ~/arctic-browning/scripts/mask_hdf.py -i ndvi.list -b '1 km monthly NDVI' -q '1 km monthly VI Quality' -t ndvi -v
rm ndvi.list 

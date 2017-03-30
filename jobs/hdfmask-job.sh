#!/bin/bash
#PBS -l nodes=1:ppn=1
#PBS -l walltime=03:00:00
#PBS -N hdfmask
#PBS -o /users/c/f/cfusting/job_logs
#PBS -e /users/c/f/cfusting/job_logs
#PBS -q shortq
cd ~/scratch/temperature
ls | egrep "*.hdf$" > temp.list
python ~/arctic-browning/scripts/mask_list.py -i temp.list -b LST_Day_1km -q QC_Day
rm temp.list

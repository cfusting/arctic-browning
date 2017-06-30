#!/bin/bash
#PBS -l nodes=1:ppn=1,pmem=8gb,pvmem=8gb
#PBS -l walltime=03:00:00
#PBS -N lst_mask
#PBS -o /users/c/f/cfusting/job_logs
#PBS -e /users/c/f/cfusting/job_logs
#PBS -q shortq
source $HOME/.bash_profile
export PYTHONPATH=$HOME/gp_mecl:$HOME/arctic-browning
directory=${MODIS_DATA_HOME}/lst_8day_1km_new
cd ${directory}
find `pwd` -name "*hdf" > hdfs.list
python ~/arctic-browning/scripts/hdf/mask_hdf.py -i ${directory}/hdfs.list -b LST_Day_1km -q QC_Day -t lst -v

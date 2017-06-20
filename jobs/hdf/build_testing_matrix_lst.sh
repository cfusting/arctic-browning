#!/bin/bash
#PBS -l nodes=1:ppn=1,pmem=32gb,pvmem=32gb
#PBS -l walltime=01:00:00
#PBS -N test_matrix
#PBS -o /users/c/f/cfusting/job_logs
#PBS -e /users/c/f/cfusting/job_logs
#PBS -q shortq
source ~/.bash_profile
uphdfs
filename="testing_matrix_lst.hdf"
rm $ARCTIC_DATA/$filename
export PYTHONPATH=$HOME/gp_mecl:$HOME/arctic-browning
python $ARCTIC_HOME/scripts/hdf/design_matrix.py \
-l $MODIS_DATA_HOME"/lst_8day_1km/hdfs.list" \
-n $MODIS_DATA_HOME"/ndvi_monthly_1km/hdfs.list" \
-y 2015 -j 2016 -t 255 -a 365 -e 0 -o $ARCTIC_DATA_HOME/$filename -v

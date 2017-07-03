#!/bin/bash
#PBS -l nodes=1:ppn=1,pmem=64gb,pvmem=64gb
#PBS -l walltime=03:00:00
#PBS -N training_matrix
#PBS -o /users/c/f/cfusting/job_logs
#PBS -e /users/c/f/cfusting/job_logs
#PBS -q shortq
source ~/.bash_profile
uphdfs
filename="training_matrix_lst_snow_2001_2016.hdf"
rm $ARCTIC_DATA/$filename
export PYTHONPATH=$HOME/gp_mecl:$ARCTIC_HOME
python $ARCTIC_HOME"/scripts/hdf/design_matrix.py" \
-l $MODIS_DATA_HOME"/lst_8day_1km/hdfs.list" \
-n $MODIS_DATA_HOME"/ndvi_monthly_1km/hdfs.list" \
-s $MODIS_DATA_HOME"/snow_8day_500m/hdfs.list" \
-y 2002 -j 2016 -t 245 -a 360 -e 0 -o $ARCTIC_DATA_HOME/$filename -v -m .2 -z .98

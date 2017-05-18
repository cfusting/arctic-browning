#!/bin/bash
#PBS -l nodes=1:ppn=1,pmem=32gb,pvmem=32gb
#PBS -l walltime=03:00:00
#PBS -N training_matrix
#PBS -o /users/c/f/cfusting/job_logs
#PBS -e /users/c/f/cfusting/job_logs
#PBS -q shortq
source ~/.bash_profile
uphdfs
filename="training_matrix.hdf"
rm $ARCTIC_DATA/$filename
export PYTHONPATH=$HOME/gp_mecl:$ARCTIC_HOME
python $ARCTIC_HOME"/scripts/hdf/design_matrix.py" \
-l $MODIS_DATA_HOME"/lst_8day_1km/hdfs.list" \
-n $MODIS_DATA_HOME"/ndvi_monthly_1km/hdfs.list" \
-s $MODIS_DATA_HOME"/snow_8day_500m/hdfs.list" \
-y 2011 -j 2014 -t 255 -a 365 -e 0 -o $ARCTIC_DATA_HOME/$filename -v -m .3 -z .98 -d

#!/bin/bash
#PBS -l nodes=1:ppn=1,pmem=64gb,pvmem=64gb
#PBS -l walltime=03:00:00
#PBS -N training_matrix
#PBS -o /users/c/f/cfusting/job_logs
#PBS -e /users/c/f/cfusting/job_logs
#PBS -q shortq
source ~/.bash_profile
uphdfs
training=training_matrix_lst_snow_${start}_${end}_${prop}.hdf
testing=testing_matrix_lst_snow_${tstart}_${tend}_${prop}.hdf
start=2002
end=2013
tstart=2014
tend=2016
prop=.15
rm ${ARCTIC_DATA}/${training}
rm ${ARCTIC_DATA}/${testing}
export PYTHONPATH=${HOME}/gp_mecl:${ARCTIC_HOME}
python ${ARCTIC_HOME}/scripts/hdf/design_matrix.py \
-l ${MODIS_DATA_HOME}/lst_8day_1km/hdfs.list \
-n ${MODIS_DATA_HOME}/ndvi_monthly_1km/hdfs.list \
-s ${MODIS_DATA_HOME}/snow_8day_500m/hdfs.list \
-y ${start} -j ${tend} -b ${tstart} -t 245 -a 360 -e 0 \
-v -m ${prop} -z .98 \
-o ${ARCTIC_DATA_HOME}/${training} \
-q ${ARCTIC_DATA_HOME}/${testing}

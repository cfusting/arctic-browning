#!/bin/bash
#PBS -l nodes=1:ppn=1,pmem=8gb,pvmem=8gb
#PBS -l walltime=30:00:00
#PBS -N symbolic
#PBS -o /users/c/f/cfusting/job_logs
#PBS -e /users/c/f/cfusting/job_logs
source $HOME/.bash_profile
export PYTHONPATH=$HOME/gp_mecl:$ARCTIC_HOME
folder=${training}_${experiment}
mkdir ${ARCTIC_RESULTS_HOME}/${folder}
cd ${ARCTIC_RESULTS_HOME}/${folder}
config=${folder}_config
cp -r ${ARCTIC_HOME}/experiments ${config}
python ${ARCTIC_HOME}/scripts/ml/symbolic_regression.py -t "${ARCTIC_DATA_HOME}/${training}" -s ${seed} -e ${experiment} -p ${split}

#!/bin/bash
#PBS -l nodes=1:ppn=1,pmem=2gb,pvmem=2gb
#PBS -l walltime=00:15:00
#PBS -N symbolic_validate
#PBS -o /users/c/f/cfusting/job_logs
#PBS -e /users/c/f/cfusting/job_logs
#PBS -q shortq
source $HOME/.bash_profile
export PYTHONPATH=$HOME/gp_mecl:$ARCTIC_HOME
python ${ARCTIC_HOME}/scripts/results/symbolic_validate.py \
        -t ${ARCTIC_DATA_HOME}/${dataset}.${datatype} \
        -j ${ARCTIC_DATA_HOME}/${dataset}.${datatype} \
        -e ${experiment} \
        -r ${ARCTIC_RESULTS_HOME}/${dataset}.${datatype}_${experiment}
python ${ARCTIC_HOME}/scripts/plotting/frequent_features.py \
        -t ${ARCTIC_DATA_HOME}/${dataset}.${datatype} \
        -e ${experiment} \
        -r ${ARCTIC_RESULTS_HOME}/${dataset}.${datatype}_${experiment}

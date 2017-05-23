#!/bin/bash
#PBS -l nodes=1:ppn=1,pmem=32gb,pvmem=32gb
#PBS -l walltime=30:00:00
#PBS -N symbolic_validate
#PBS -o /users/c/f/cfusting/job_logs
#PBS -e /users/c/f/cfusting/job_logs
source $HOME/.bash_profile
export PYTHONPATH=$HOME/gp_mecl:$ARCTIC_HOME
python "$ARCTIC_HOME/scripts/ml/symbolic_validate.py" -r $directory -v -n $name -t $ARCTIC_DATA_HOME/training_matrix.hdf -j $ARCTIC_DATA_HOME/testing_matrix.hdf

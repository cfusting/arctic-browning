#!/bin/bash
#PBS -l nodes=1:ppn=1,pmem=32gb,pvmem=32gb
#PBS -l walltime=30:00:00
#PBS -N frequent_features
#PBS -o /users/c/f/cfusting/job_logs
#PBS -e /users/c/f/cfusting/job_logs
source $HOME/.bash_profile
export PYTHONPATH=$HOME/gp_mecl:$ARCTIC_HOME
python "$ARCTIC_HOME/scripts/plotting/frequent_features.py" -r $directory -n $name -t $ARCTIC_DATA_HOME/training_matrix.hdf
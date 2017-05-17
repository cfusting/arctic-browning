#!/bin/bash
#PBS -l nodes=1:ppn=1,pmem=32gb,pvmem=32gb
#PBS -l walltime=03:00:00
#PBS -N symbolic_validate
#PBS -o /users/c/f/cfusting/job_logs
#PBS -e /users/c/f/cfusting/job_logs
#PBS -q shortq
export PYTHONPATH=$HOME/gp_mecl:$HOME/arctic-browning
python "$HOME/arctic-browning/scripts/ml/symbolic_validate.py" -n $name -t $MODIS_DATA_HOME/training_matrix.hdf -j MODIS_DATA_HOME/testing_matrix.hdf -r $ARCTIC_RESULTS_HOME

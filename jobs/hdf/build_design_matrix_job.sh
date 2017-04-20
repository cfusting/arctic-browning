#!/bin/bash
#PBS -l nodes=1:ppn=1,pmem=32gb,pvmem=32gb
#PBS -l walltime=01:00:00
#PBS -N dmatrix
#PBS -o /users/c/f/cfusting/job_logs
#PBS -e /users/c/f/cfusting/job_logs
#PBS -q shortq
source $HOME/arctic-browning/scripts/hdf/build_design_matrix.sh

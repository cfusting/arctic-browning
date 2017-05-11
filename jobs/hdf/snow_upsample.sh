#!/bin/bash
#PBS -l nodes=1:ppn=1,pmem=8gb,pvmem=8gb
#PBS -l walltime=00:15:00
#PBS -N snow_upsample
#PBS -o /users/c/f/cfusting/job_logs
#PBS -e /users/c/f/cfusting/job_logs
export PYTHONPATH=$HOME/gp_mecl:$HOME/arctic-browning
python ~/arctic-browning/scripts/hdf/upsample_snow.py -f $filepath -l masked_Maximum_Snow_Extent -v
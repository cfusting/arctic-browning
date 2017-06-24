#!/bin/bash
#PBS -l nodes=1:ppn=1,pmem=2gb,pvmem=2gb
#PBS -l walltime=00:15:00
#PBS -N replace_variables
#PBS -o /users/c/f/cfusting/job_logs
#PBS -e /users/c/f/cfusting/job_logs
#PBS -q shortq
sed -r -i 's/(lst|snow)_([0-9]+)/\1\2/g' ${filepath}
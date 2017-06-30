#!/bin/bash
#PBS -l nodes=1:ppn=1
#PBS -l walltime=03:00:00
#PBS -N get-data
#PBS -q shortq
#PBS -e /users/c/f/cfusting/job_logs
#PBS -o /users/c/f/cfusting/job_logs
modis_download.py -r -D 1 -U cfusting -P Blueferret1 -t $tile -p $dataset -f 2010-01-01 -e 2010-12-31 $directory

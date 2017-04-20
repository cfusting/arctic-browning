#!/bin/bash
#PBS -l nodes=1:ppn=1
#PBS -l walltime=03:00:00
#PBS -N get-data
#PBS -q shortq
#PBS -e /users/c/f/cfusting/job_logs
#PBS -o /users/c/f/cfusting/job_logs
cd $HOME"/scratch"
mkdir $directory
modis_download.py -r -D 1 -u $url -s $source -U cfusting -P Blueferret1 -t $tile -p $dataset -f 2011-01-01 -e 2014-12-31 $directory

#!/bin/bash
#PBS -l nodes=1:ppn=1
#PBS -l walltime=03:00:00
#PBS -N get-data
#PBS -q shortq
#PBS -e /users/c/f/cfusting/job_logs
#PBS -o /users/c/f/cfusting/job_logs
source /users/c/f/cfusting/.bash_profile
source /users/c/f/cfusting/geospatial/bin/activate
python $SCRIPT -s 2011 -e 2014 -f $firstday -l lastday -d $directory -k 'clipped_mosaic.*NDVI' -r 'clipped_mosaic.*Quality' -j '\d{7}' -v -b $HOME/job_logs/temporal_stats.log >> $NDVIOUT

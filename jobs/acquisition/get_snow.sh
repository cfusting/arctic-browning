#!/bin/bash
#PBS -l nodes=1:ppn=1
#PBS -l walltime=03:00:00
#PBS -N get-snow
#PBS -q shortq
#PBS -e /users/c/f/cfusting/job_logs
#PBS -o /users/c/f/cfusting/job_logs
python ~/arctic-browning/scripts/acquisition/snow_data.py -s 2010.01.01 -e 2016.12.31 -d $HOME/modis_data/snow_8day_500m/ -t h20v02 -u cfusting -p Blueferret1

##!/bin/bash
# Variables to pass in:
# year - The year to process.
#PBS -l nodes=1:ppn=1,pmem=20gb,pvmem=20gb
#PBS -l walltime=03:00:00
#PBS -q shortq
#PBS -N extract-ndvi
#PBS -o /users/c/f/cfusting/job_logs
#PBS -e /users/c/f/cfusting/job_logs
source $HOME"/.bash_profile"
source $HOME"/geospatial/bin/activate"
SCRIPT=$HOME"/arctic-browning/scripts/temporal_statistics.py"
DIRECTORY=$HOME"/scratch/ndvi_monthly/mosaics/${year}"
NDVIOUT=$DIRECTORY"/${year}.csv"
echo "year,tindvi,weight" > $NDVIOUT
python $SCRIPT -s ${year} -e ${year} -f 152 -l 244 -d $DIRECTORY -k '.*NDVI.*' -r '.*Quality.*' -j '\d{7}' -v -n -b $HOME/job_logs/temporal_stats.log > $NDVIOUT

#!/bin/bash
#PBS -l nodes=1:ppn=1
#PBS -l walltime=03:00:00
#PBS -q shortq
#PBS -N modis-convert
#PBS -o /users/c/f/cfusting/job_logs
#PBS -e /users/c/f/cfusting/job_logs
source /users/c/f/cfusting/.bash_profile
source /users/c/f/cfusting/geospatial/bin/activate
cd $directory
mkdir mosaics
ids=$(ls | grep -oh "\.A[0-9]*[0-9]\." | sed 's/\.//g' | uniq)
for i in $ids
do
    ls | grep $i".*hdf$" > $i".filelist"
	source $HOME/arctic-browning/scripts/convert.sh $i".filelist"
    rm $i".filelist"
done

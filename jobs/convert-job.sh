#!/bin/bash
#PBS -l nodes=1:ppn=1
#PBS -l walltime=03:00:00
#PBS -N modis-convert
source /users/c/f/cfusting/.bash_profile
source /users/c/f/cfusting/geospatial/bin/activate
cd $directory
mkdir mosaics
ids=$(ls | grep -oh A[0-9]*[0-9] | sort | uniq)
for i in $ids
do
    ls | grep $i".*hdf$" > $i".filelist"
	source $HOME/arctic-browning/scripts/convert.sh $i".filelist"
    rm $i".filelist"
done

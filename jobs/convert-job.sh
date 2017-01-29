#!/bin/bash
#PBS -l nodes=1:ppn=1
#PBS -l walltime=10:00:00
#PBS -N modis-convert
cd $HOME/v5_ndvi_terra
ids=$(ls | grep -oh A[0-9]*[0-9] | sort | uniq)
for i in $ids
do
        ls | grep $i".*hdf$" > $i".filelist"
	source $HOME/arctic-browning/scripts/convert.sh $i".filelist" 
        rm $i".filelist"
done

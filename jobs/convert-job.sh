#!/bin/bash
#PBS -l nodes=1:ppn=1
#PBS -l walltime=10:00:00
#PBS -N modis-convert
cd $HOME/ndvi_terra
ids=$(ls | grep -oh A[0-9]*[0-9] | uniq)
for i in $ids
do
        ls | grep $i".*hdf$" > $i".filelist"
	source $HOME/browning/scripts/convert.sh $i".filelist" 
        rm $i".filelist"
done

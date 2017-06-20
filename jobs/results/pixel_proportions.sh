#!/bin/bash
counter=1
for i in `seq 1 32 365`
do
    lastday=`expr $i + 24`
    if [ $lastday -eq 377 ]
    then
      lastday=361
    fi
    outdir="lst_pa_"$i"_"$lastday
    qsub -v directory=/users/c/f/cfusting/scratch/temperature/mosaics,firstday=$i,lastday=$lastday,outdir=$outdir $HOME"/arctic-browning/scripts/plotting/pixel_proportions.sh"
    let counter=counter+32
done

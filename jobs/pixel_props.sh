#!/bin/bash
# Variables to define:
# directory - where the data resides.
#PBS -l nodes=1:ppn=1
#PBS -l walltime=03:00:00
#PBS -N pixel-props
#PBS -q shortq
#PBS -e /users/c/f/cfusting/job_logs
#PBS -o /users/c/f/cfusting/job_logs
source /users/c/f/cfusting/.bash_profile
source /users/c/f/cfusting/modis/bin/activate
counter=1
for i in `seq 1 32 365`
do
    lastday=`expr $i + 24`
    if [ $lastday -eq 377 ]
    then
      lastday=361
    fi
    outdir="lst_pa_"$i"_"$lastday
    echo python $HOME"/arctic-browning/scripts/pixel_plots.py" -s 2011 -e 2014 -f $i -l $lastday -d $directory -k 'LST_Day' -r 'QC_Day' -j '\d{7}' -v -b $HOME"/job_logs/pixel_props.log" -o $HOME"/scratch/"$outdir"/"$outdir -z $HOME"/scratch/"$outdir
    let counter=counter+32
done

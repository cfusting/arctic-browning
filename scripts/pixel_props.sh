#!/bin/bash
# Variables to define:
# directory - where the data resides.
#PBS -l nodes=1:ppn=1,pmem=4gb,pvmem=4gb
#PBS -l walltime=03:00:00
#PBS -N pixel-props
#PBS -q shortq
#PBS -e /users/c/f/cfusting/job_logs
#PBS -o /users/c/f/cfusting/job_logs
source /users/c/f/cfusting/.bash_profile
source /users/c/f/cfusting/modis/bin/activate
destdir=$HOME"/scratch/"$outdir
mkdir $destdir
python $HOME"/arctic-browning/scripts/pixel_plots.py" -s 2011 -e 2014 -f $firstday -l $lastday -d $directory -k 'LST_Day' -r 'QC_Day' -j '\d{7}' -v -b $HOME"/job_logs/pixel_props_"$outdir".log" -o $destdir"/"$outdir -z $destdir"/"


#!/bin/bash
#PBS -l nodes=1:ppn=1
#PBS -l walltime=10:00:00
#PBS -N get-data
source /users/c/f/cfusting/.bash_profile
source /users/c/f/cfusting/modis/bin/activate
mkdir $directory
modis_download.py -I -r -t $tile -p $dataset -f 2011-01-01 -e 2014-12-31 $directory

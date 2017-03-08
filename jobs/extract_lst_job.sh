#!/usr/bin/env bash
#PBS -l nodes=1:ppn=1
#PBS -l walltime=01:00:00
#PBS -N extract-data
#PBS -o /users/c/f/cfusting/job_logs
#PBS -e /users/c/f/cfusting/job_logs
source /users/c/f/cfusting/.bash_profile
source /users/c/f/cfusting/geospatial/bin/activate
python ~/arctic-browning/scripts/extract_data.py -i ${input} -q ${quality} > "${doy}.csv"
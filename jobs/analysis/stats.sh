#!/bin/bash
#PBS -l nodes=1:ppn=1
#PBS -N getstats 
#PBS -l walltime=04:00:00
#PBS -e /users/c/f/cfusting/job_logs
#PBS -o /users/c/f/cfusting/job_logs
source $HOME/browning/scripts/analysis/statistics.sh

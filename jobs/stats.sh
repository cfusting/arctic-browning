#!/bin/bash
#PBS -l nodes=1:ppn=1
#PBS -N getstats 
#PBS -l walltime=04:00:00
source $HOME/browning/scripts/statistics.sh

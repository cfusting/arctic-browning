#!/bin/bash
#PBS -l nodes=1:ppn=1
#PBS -N getstats 
#PBS -l walltime=01:00:00
source $HOME/arctic-browning/scripts/temporal_statistics.sh

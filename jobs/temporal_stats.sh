#!/bin/bash
#PBS -l nodes=1:ppn=1,pmem=32gb,pvmem=32gb
#PBS -N get_temporal_stats 
#PBS -l walltime=03:00:00
#PBS -q shortq
source $HOME/arctic-browning/scripts/temporal_statistics.sh

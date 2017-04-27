#!/bin/bash
#PBS -l nodes=1:ppn=1,pmem=8gb,pvmem=8gb
#PBS -l walltime=07:00:00
#PBS -N symbolic
#PBS -o /users/c/f/cfusting/job_logs
#PBS -e /users/c/f/cfusting/job_logs
#PBS -M sam.kriegman@uvm.edu
export PYTHONPATH=$HOME/gp_mecl:$HOME/arctic-browning
cd $HOME/symbolic_results
python $HOME/arctic-browning/scripts/ml/symbolic_regression.py -t $training -s $seed -n $name

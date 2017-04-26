#!/bin/bash
#PBS -l nodes=1:ppn=1,pmem=8gb,pvmem=8gb
#PBS -l walltime=03:00:00
#PBS -N symbolic_results
#PBS -o /users/c/f/cfusting/job_logs
#PBS -e /users/c/f/cfusting/job_logs
#PBS -q shortq
export PYTHONPATH=$HOME/gp_mecl:$HOME/arctic-browning
cd "$HOME/symbolic_evaluations"
python "$HOME/arctic-browning/scripts/ml/symbolic_results.py" -v $validate -n $name -r $results
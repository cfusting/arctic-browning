#!/bin/bash
#PBS -l nodes=1:ppn=1,pmem=2gb,pvmem=2gb
#PBS -l walltime=00:15:00
#PBS -N replace_terminals
#PBS -o /users/c/f/cfusting/job_logs
#PBS -e /users/c/f/cfusting/job_logs
#PBS -q shortq
sed -r -i 's/([a-zA-Z]+Operation)\(([a-zA-Z0-9]+?),([a-zA-Z0-9]+?),([a-zA-Z0-9]+?)\)/\1_\2_\3_\4/g' pareto*

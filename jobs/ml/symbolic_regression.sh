#!/bin/bash
#PBS -l nodes=1:ppn=1,pmem=8gb,pvmem=8gb
#PBS -l walltime=30:00:00
#PBS -N symbolic
#PBS -o /users/c/f/cfusting/job_logs
#PBS -e /users/c/f/cfusting/job_logs
source $HOME/.bash_profile
export PYTHONPATH=$HOME/gp_mecl:$ARCTIC_HOME
cd $ARCTIC_RESULTS_HOME
config=$name"_config.log"
cp $ARCTIC_HOME/experiments/$name.py $config
cp $ARCTIC_HOME/experiments/utils.py $name"_utils.py"
echo ----DATA---- >> $config
echo $training >> $config
python $ARCTIC_HOME/scripts/ml/symbolic_regression.py -t $training -s $seed -e $experiment

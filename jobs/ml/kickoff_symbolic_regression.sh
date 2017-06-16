#!/bin/bash
# usage: source kickoff_symbolic_regression experiment_name num_runs data
last=`pwd`
cd $ARCTIC_RESULTS_HOME
for i in `seq 1 $2`
do
	seed=$RANDOM
	qsub -v training=$3,seed=$seed,experiment=$1 "$ARCTIC_HOME/jobs/ml/symbolic_regression.sh"
	echo "Run $i: $1 started with seed $seed"
done
cd $last

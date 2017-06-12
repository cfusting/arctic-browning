#!/bin/bash
# usage: source kickoff_symbolic_regression experiment_name num_runs
for i in `seq 1 $2`
do
	seed=$RANDOM
	qsub -v training=$ARCTIC_DATA_HOME/linear_combination.csv,seed=$seed,name=$1 "$ARCTIC_HOME/jobs/ml/synthetic_symbolic_regression.sh"
	echo "Run $i: $1 started with seed $seed"
done

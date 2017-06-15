#!/bin/bash
# usage: source kickoff_symbolic_regression experiment_name num_runs
last=`pwd`
cd $ARCTIC_RESULTS_HOME
for i in `seq 1 $2`
do
	seed=$RANDOM
	qsub -v training=$ARCTIC_DATA_HOME/training_matrix.hdf,seed=$seed,name=$1 "$ARCTIC_HOME/jobs/ml/symbolic_regression.sh"
	echo "Run $i: $1 started with seed $seed"
done
cd $last

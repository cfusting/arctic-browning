#!/bin/bash
# usage: source kickoff_symbolic_regression experiment_name num_runs data split
last=`pwd`
for i in `seq 1 ${2}`
do
	seed=${RANDOM}
	qsub -v training=${3},seed=${seed},experiment=${1},split=${4} "${ARCTIC_HOME}/jobs/ml/symbolic_regression.sh"
	echo "Run ${i}: ${1} started with seed ${seed}"
done
cd ${last}

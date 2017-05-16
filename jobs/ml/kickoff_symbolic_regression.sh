#!/bin/bash
# usage training_data name runs
for i in `seq 1 $3`
do
	seed=$RANDOM
	qsub -v training=$1,seed=$seed,name=$2 "$ARCTIC_HOME/jobs/ml/symbolic_regression.sh"
	echo "Run $i: $2 started with seed $seed"
done

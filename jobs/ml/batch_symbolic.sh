#!/bin/bash
for i in `seq 1 $3`
do
	seed=$RANDOM
	qsub -v data=$1,seed=$seed,name=$2 "$HOME/arctic-browning/jobs/ml/symbolic.sh"
	echo "Run $i: $2 started with seed $seed"
done

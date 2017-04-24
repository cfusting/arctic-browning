#!/bin/bash
for i in `seq 1 $3`
do
	seed=$RANDOM
	qsub -v data=$1,seed=$seed,name=$2 single_gp_runner.pbs
	echo "Run $i: $2 started with seed $seed"
	sleep 1;
done
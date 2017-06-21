#!/bin/bash
# trainset, testset, datatype
experiments="control mandarin whistling_duck lesser_scaup bufflehead"
for experiment in ${experiments}
do
  qsub -v experiment=${experiment},trainset=${1},testset=${2},datatype=${3} ${ARCTIC_HOME}/jobs/results/evaluate.sh
done

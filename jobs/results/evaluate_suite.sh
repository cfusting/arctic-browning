#!/bin/bash
# dataset, datatype
experiments="control mandarin whistling_duck lesser_scaup bufflehead"
for experiment in ${experiments}
do
  qsub -v experiment=${experiment},dataset=${1},datatype=${2} ${ARCTIC_HOME}/jobs/results/evaluate.sh
done

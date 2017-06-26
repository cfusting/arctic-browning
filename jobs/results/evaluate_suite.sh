#!/bin/bash
# trainset, testset, datatype, flags
#experiments="control mandarin whistling_duck bufflehead"
experiments="control"
for experiment in ${experiments}
do
  if [[ ${flags} == *"l"* ]]
  then
    trainset=${trainset} testset=${testset} datatype=${datatype} flags=${flags} experiment=${experiment} \
    ${ARCTIC_HOME}/jobs/results/evaluate.sh
  else
     qsub -N evaluate_${1}_${experiment} \
    -v experiment=${experiment},trainset=${1},testset=${2},datatype=${3},flags=${flags} \
    ${ARCTIC_HOME}/jobs/results/evaluate.sh
  fi
done

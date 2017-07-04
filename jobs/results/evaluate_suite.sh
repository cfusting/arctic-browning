#!/bin/bash
# trainset, testset, datatype, flags
#experiments="control mandarin whistling_duck"
experiments="lesser_scaup"
for experiment in ${experiments}
do
  if [[ ${flags} == *"l"* ]]
  then
    trainset=${trainset} testset=${testset} datatype=${datatype} flags=${flags} experiment=${experiment} \
    ${ARCTIC_HOME}/jobs/results/evaluate.sh
  else
    qsub -N evaluate_${1}_${experiment} \
    -v experiment=${experiment},trainset=${1},testset=${2},datatype=${3},flags=${4} \
    ${ARCTIC_HOME}/jobs/results/evaluate.sh
  fi
done

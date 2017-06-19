#!/bin/bash
# runs data split
experiments="control mandarin whistling_duck bufflehead"
for experiment in ${experiments}
do
  source ${ARCTIC_HOME}/jobs/ml/kickoff_symbolic_regression.sh ${experiment} ${1} ${2} ${3}
done

#!/bin/bash
cd $ARCTIC_RESULTS_HOME
for directory in $(ls | grep training)
do
  cd $directory
  fullpath=`pwd`
  filepath="${fullpath}/pareto*"
  echo "Replacing snow and lst variables in: ${directory}"
  qsub -v filepath=${filepath} $ARCTIC_HOME/jobs/results/replace_variables.sh
  cd ..
done
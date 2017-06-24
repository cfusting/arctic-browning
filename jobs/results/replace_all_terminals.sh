#!/bin/bash
cd $ARCTIC_RESULTS_HOME
for directory in $(ls)
do
  cd $directory
  fullpath=`pwd`
  filepath="${fullpath}/pareto*"
  echo "Fixing Range and Moment terminals in: ${directory}"
  qsub -v filepath=${filepath} $ARCTIC_HOME/jobs/results/replace_terminals.sh
  cd ..
done
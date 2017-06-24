#!/bin/bash
cd $ARCTIC_RESULTS_HOME
for directory in $(ls)
do
  cd $directory
  echo "Fixing Range and Moment terminals in: ${directory}"
  qsub $ARCTIC_HOME/jobs/results/replace_terminals.sh
  cd ..
done
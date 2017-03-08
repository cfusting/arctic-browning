#!/bin/bash
# Convert LST to CSV files.
lst=$( ls | grep "LST_Day")
qc=($( ls | grep "QC_Day"))
i=0
for f in ${lst}
do
  doy=${f:5:3}
  if [ ${doy} != ${qc[${i}]:5:3} ]
  then
    echo "LST file does not match quality file."
    exit 1
  fi
  qsub -v input=${f},quality=${qc},doy=${doy},directory=$( pwd ) ~/arctic-browning/jobs/extract_lst_job.sh
  (( i++ ))
done

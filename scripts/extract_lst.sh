#!/bin/bash
# Convert LST to CSV files.
lst=$( ls | grep "LST_DAY")
qc=($( ls | grep "QC_DAY"))
ct=0
for f in ${lst}
do
  doy=${f:5:3}
  if [ ${doy} -neq ${qc[${i}]:5:3} ]
  then
    echo "LST file does not match quality file."
    exit 1
  fi
  echo qsub -v input=${f},quality=${qc},doy=${doy} ~/arctic-browning/scripts/jobs/extract_lst_job.sh
done

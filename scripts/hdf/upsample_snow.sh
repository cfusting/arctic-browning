#!/bin/bash
for i in $(find $(pwd) -name "*hdf")
do
  qsub -v filepath=$i ~/arctic-browning/jobs/hdf/snow_upsample.sh
done

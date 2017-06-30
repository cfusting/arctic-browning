#!/bin/bash
cd ~/modis_data/snow_8day_500m_new
for i in $(find $(pwd) -name "*hdf")
do
  qsub -v filepath=$i ~/arctic-browning/jobs/hdf/snow_upsample.sh
done
cd -

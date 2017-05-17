#!/bin/bash
hdfs() {
  last=`pwd`
  cd $1
  find `pwd` -name "*hdf" > hdfs.list
  cd $last
}

uphdfs() {
  hdfs $MODIS_DATA_HOME/lst_8day_1km
  hdfs $MODIS_DATA_HOME/ndvi_monthly_1km
  hdfs $MODIS_DATA_HOME/snow_8day_500m
}

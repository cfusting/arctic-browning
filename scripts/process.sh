#!/bin/bash
# Each date has a unique id
ids=$(ls | grep -oh A[0-9]*[0-9] | uniq)
echo "$ids" > date.ids
for i in $ids; do
	ls | grep $i".*hdf$" > $i".filelist"
done

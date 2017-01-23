#!/usr/bin/env bash

#for dir in MDBA*
#do
#    for start_date in 2008 2009 2013 2014 2015
#    do
#        real_date=$(($start_date + 1))
#        find $dir -name "*$start_date0901*.tif" | gdalbuildvrt -input_file_list /vsistdin/ "${dir}_${real_date}.vrt"
#
#    done
#done

for file in `find -name '*20080901*.tif'`
do
    echo `gdalinfo -json $file | jq '.bands | length'` $file
#    echo `rio info $file |  jq '.count'` $file
done

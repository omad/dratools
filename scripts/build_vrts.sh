#!/usr/bin/env bash


#for dir in MDBA_PCT_??
for dir in MDBA_PCT_25
do
#    for start_date in 2008 2009 2013 2014 2015
    for start_date in 2013 2014 2015
    do
        real_date=$(($start_date + 1))
        echo find $dir -name "*${start_date}0901*.tif"
        find $dir -name "*${start_date}0901*.tif" | gdalbuildvrt -input_file_list /vsistdin/ "${dir}_${real_date}.vrt"

    done
done


# Stack Cells
for dir in MDBA_PCT_??
do
    for cell in -40 -39
    do
        for start_date in 2008 2009
        do
            for datatype in observed_date clear_obs
            do
                real_date=$(($start_date + 1))
                echo find $dir -name "*_${cell}*${datatype}*${start_date}0901*.tif"
                find $dir -name "*${cell}*${datatype}*${start_date}0901*.tif" | gdalbuildvrt -separate -input_file_list /vsistdin/ "${dir}/SR_LS5_N_PCT_25_3577_12_${cell}_${real_date}_${datatype}.vrt"
            done
        done
    done
done

#for dir in MDBA_PCT_??
#for dir in MDBA_PCT_25
#do
#    for start_date in 2008 2009 2013 2014 2015
#    for start_date in 2013 2014 2015
#    for real_date in 2009 2010
#    do
##        real_date=$(($start_date + 1))
#        echo find $dir -name "*${start_date}0901*.tif"
#        find $dir -name "*${start_date}0901*.tif" | gdalbuildvrt -input_file_list /vsistdin/ "${dir}_${real_date}.vrt"
#
#    done
#done

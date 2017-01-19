#!/usr/bin/env bash


for stat in mean min max; do
    python ~/src/agdc-v2/datacube_apps/stats/stack.py NDWI_STATS/ndwi*$stat*0301.tif -o stacked/ARG25_16_-33_EPSG3577_1985_2016_MAR_MAY_NDWI_$stat.tif
    python ~/src/agdc-v2/datacube_apps/stats/stack.py NDWI_STATS/ndwi*$stat*0601.tif -o stacked/ARG25_16_-33_EPSG3577_1985_2016_JUN_AUG_NDWI_$stat.tif
    python ~/src/agdc-v2/datacube_apps/stats/stack.py NDWI_STATS/ndwi*$stat*0901.tif -o stacked/ARG25_16_-33_EPSG3577_1985_2016_SEP_NOV_NDWI_$stat.tif
    python ~/src/agdc-v2/datacube_apps/stats/stack.py NDWI_STATS/ndwi*$stat*1201.tif -o stacked/ARG25_16_-33_EPSG3577_1985_2016_DEC_FEB_NDWI_$stat.tif
done

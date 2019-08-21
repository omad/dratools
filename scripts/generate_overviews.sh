#!/usr/bin/env bash


tasks=''
#echo Generating overviews for individual tiff files
for file in `find . -name '*.tif'`; do
    if [ $file -nt ${file}.ovr ]; then
#        echo 'Making overviews for ' $file
        tasks="${tasks}time gdaladdo -ro --config COMPRESS_OVERVIEW DEFLATE $file 2 4 8\n"
#        time gdaladdo -ro --config USE_RRD YES --config COMPRESS_OVERVIEW DEFLATE $file 2 4 8
    fi
done

echo -e $tasks


#echo tmux \\
#for vrt in *.vrt
#do
##    echo 'Making overviews for ' $vrt
#    echo "split-window 'gdaladdo -ro --config COMPRESS_OVERVIEW DEFLATE $vrt 16 32 64' \\; \\"
#done

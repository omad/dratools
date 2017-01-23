#!/usr/bin/env python3
"""
Generate gdal VRTs of netcdfs that can be viewed as RGB/etc in QGIS.

"""
import sys
from glob import glob
import subprocess
from tqdm import tqdm
from pathlib import Path

import concurrent.futures

COLOURS = 'blue green red nir swir1 swir2'.split()
MAX_WORKERS = 8


def build_netcdf_vrts(pattern):
    print("Building viewable VRTs")
    vrts = []
    for filename in tqdm(glob(pattern, recursive=True)):
        vrt_name = filename.replace('.nc', '.vrt')
        vrt_path = Path(vrt_name)
        vrts.append(vrt_name)

        if not vrt_path.exists() or Path(filename).stat().st_mtime > vrt_path.stat().st_mtime:
            input_layers = ['NETCDF:{}:{}'.format(filename, colour) for colour in COLOURS]
            subprocess.run(['gdalbuildvrt', '-separate', vrt_name] + input_layers, check=True, stdout=subprocess.DEVNULL)
    return vrts


def build_overview(filename, levels=None):
    if not levels:
        levels = ['2', '4', '8', '16']
    return subprocess.run(['gdaladdo', '-ro', filename] + levels, check=True, stdout=subprocess.DEVNULL)


def build_overviews(tile_files):
    print("Building Tiles overviews")
    with concurrent.futures.ProcessPoolExecutor(max_workers=MAX_WORKERS) as executor:
        num_files = len(tile_files)
        results = executor.map(build_overview, tile_files)

        completed = [done for done in tqdm(results, total=num_files)]


def mosaic_vrt(output_name, filenames):
    levels = ['32', '64', '128']
    print('Building VRT Mosaic')
    subprocess.run(['gdalbuildvrt', output_name] + filenames, check=True)
    print('Building Mosaic Overviews')
    subprocess.run(['gdaladdo', '--config', 'COMPRESS_OVERVIEW', 'DEFLATE', output_name] + levels, check=True)


def main():
    pattern = sys.argv[1]

    if pattern[-2:] == 'nc':
        tile_files = build_netcdf_vrts(pattern)
    else:
        tile_files = list(glob(pattern, recursive=True))

    build_overviews(tile_files)

    output_name = sys.argv[2]
    mosaic_vrt(output_name, tile_files)


if __name__ == '__main__':
    main()

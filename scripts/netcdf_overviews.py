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

path = sys.argv[1]
# overall_vrt = sys.argv[2]

COLOURS = 'blue green red nir swir1 swir2'.split()

print("Building viewable VRTs")
for filename in tqdm(glob('{}/**/*.nc'.format(path), recursive=True)):
    vrt_name = filename.replace('.nc', '.vrt')
    vrt_path = Path(vrt_name)
    vrt_outdated = Path(filename).stat().st_mtime > vrt_path.stat().st_mtime

    if not vrt_path.exists() or vrt_outdated:
        input_layers = ['NETCDF:{}:{}'.format(filename, colour) for colour in COLOURS]
        subprocess.run(['gdalbuildvrt', '-separate', vrt_name] + input_layers, check=True, stdout=subprocess.DEVNULL)


print("Building VRT overviews")
# for filename in tqdm(glob('{}/**/*.vrt'.format(path), recursive=True)):
#     subprocess.run(['gdaladdo', '-ro', filename, '2', '4', '8', '16'])


def build_overview(filename, levels=None):
    if not levels:
        levels = ['2', '4', '8', '16']
    return subprocess.run(['gdaladdo', '-ro', filename] + levels, check=True, stdout=subprocess.DEVNULL)

with concurrent.futures.ProcessPoolExecutor(max_workers=8) as executor:
    vrt_filenames = glob('{}/**/*.vrt'.format(path), recursive=True)
    num_files = len(vrt_filenames)
    results = executor.map(build_overview, vrt_filenames)

    completed = [done for done in tqdm(results, total=num_files)]



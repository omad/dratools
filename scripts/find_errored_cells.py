#!/usr/bin/env python

import re
import subprocess

regex = re.compile(r'.*Completed \(([-\d]*), ([-\d]*)\)')
completed_tiles = set()
with open('ls8_medoid_mosaic.e1101580') as logfile:
    for line in logfile:
        if 'Completed' in line:
            #            print(line)
            match = regex.search(line)
            cell = tuple(int(g) for g in match.groups())
            completed_tiles.add(cell)

cmd = 'find /home/547/dra547/shared_home/statstests/LS8_2014_FC_MEDOID -name *.tiff -size -100000c'.split()

small_file_cells = set()
regex = re.compile(r'.*_(-?\d{1,2})_(-?\d{1,2})_.*')
result = subprocess.run(cmd, stdout=subprocess.PIPE, universal_newlines=True)
for line in result.stdout.split('\n'):
    match = regex.search(line)
    if match:
        cell = tuple(int(g) for g in match.groups())
        small_file_cells.add(cell)

print('small_file_cells', len(small_file_cells))

maybe_missing = small_file_cells - completed_tiles

print('maybe_missing', len(maybe_missing))
# for x, y in maybe_missing:
#    cmd = 'find /home/547/dra547/shared_home/statstests/LS8_2014_FC_MEDOID -name *{}_{}*.tiff -size -100000c -delete'.format(x, y).split()
#    result = subprocess.run(cmd, stdout=subprocess.PIPE, universal_newlines=True)
#
#    print(result)



import netCDF4
import sys
import numpy as np

FILENAME = sys.argv[1]
DATASET_VARIABLE = 'dataset'
TIME_INDEX = 0

with netCDF4.Dataset(FILENAME) as nco:
    print(np.char.decode(netCDF4.chartostring(nco.variables[DATASET_VARIABLE][TIME_INDEX])))


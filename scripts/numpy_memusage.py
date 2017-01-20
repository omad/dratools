
import xarray as xr
from xarray.core.pycompat import iteritems
import numpy as np

@profile
def test_load():
    datasets = [make_xarray(time_start=i*100) for i in range(2)]

    datasets = xr.concat(datasets, dim='time')  # Copies all the data
    return inplace_isel(datasets, time=datasets.time.argsort())
    # return datasets.isel(time=datasets.time.argsort())  # sort along time dim  # Copies all the data again

@profile
def make_xarray(time_length=25, time_start=0):
    data = np.empty([time_length, 4000, 4000], dtype=float)
    return xr.Dataset({'blue': (('time', 'y', 'x'), data)}, {'time': list(range(time_start, time_start + time_length))})

@profile
def inplace_isel(dataset, **indexers):
    invalid = [k for k in indexers if k not in dataset.dims]
    if invalid:
        raise ValueError("dimensions %r do not exist" % invalid)

    # all indexers should be int, slice or np.ndarrays
    indexers = [(k, (np.asarray(v)
                     if not isinstance(v, (int, np.integer, slice))
                     else v))
                for k, v in iteritems(indexers)]

    for name, var in iteritems(dataset._variables):
        var_indexers = dict((k, v) for k, v in indexers if k in var.dims)
        dataset._variables[name] = var.isel(**var_indexers)
    return dataset

x = test_load()

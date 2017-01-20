

from datacube_stats.statistics import _reduce_across_variables
from hdmedians.fast import nangeomedian, nangeomedian_axis_one
from hdmedians.slow import nangeomedian
import xarray
import numpy as np

import pstats, cProfile


DATA_FILE = '/g/data/u46/users/dra547/sample_geomedian_data.nc'
dataset = xarray.open_dataset(DATA_FILE)
dataset = dataset.isel(x=slice(None, None, 100), y=slice(None, None, 100))
flattened = dataset.to_array(dim='variable')

def xarray_reduce():
    hdmedian_out = flattened.reduce(_reduce_across_variables, dim='time', keep_attrs=True, method=nangeomedian)


def simple_reduce(data, shape):
    out = np.ndarray((6, 10, 10))

    for y in range(10):
        for x in range(10):
            out[:, y, x] = nangeomedian(data[:, :, y, x])


def profile(data):
    cProfile.runctx("simple_reduce(data)", globals(), locals(), "Profile.prof")

    s = pstats.Stats("Profile.prof")
    s.strip_dirs().sort_stats("time").print_stats()


def line_profile():
    sampledata = flattened.data[:, :, 0, 0]


    import line_profiler
    profile = line_profiler.LineProfiler(nangeomedian_axis_one)
    # profile.add_function(nangeomedian_axis_one)
    # profile.runcall(nangeomedian_axis_one, sampledata)
    profile.run('simple_reduce()')

    profile.print_stats()


# band, time, y, x

profile(flattened.data)

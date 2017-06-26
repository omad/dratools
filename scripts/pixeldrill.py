#!/bin/env python3

import datacube
from datacube.api.query import query_group_by
import pandas as pd
from functools import partial
import click


@click.command(name='pixeldrill')
@click.option('--filter_value-value', '-f', type=(str, int))
@click.option('--time-period', '-t', type=(str, str), help='<start-date> <stop-date>')
@click.argument('product', type=str)
@click.argument('lat', type=float)
@click.argument('lon', type=float)
def main(lat, lon, product, filter_value=None, time_period=None):
    dc = datacube.Datacube()
    load = partial(load_with_meta, dc)

    data = load(product=product,
                time=time_period,
                lon=lon, lat=lat)
    # data = load(product='ls8_pq_albers',
    #             time=('2000-01-01', '2018-01-01'),
    #             lon=146.33, lat=-41.87)

    if filter_value:
        measurement, value = filter_value
        data = xr_filter_value(data, measurement, value)

    df = pd.DataFrame.from_dict(xr_to_dict_list(data))

    with pd.option_context('display.width', 120, 'display.max_colwidth', 120):
        print(df)


def load_with_meta(dc, *args, **kwargs):
    vals = dc.load(*args, **kwargs)
    datasets = dc.find_datasets(*args, **kwargs)
    sources = dc.group_datasets(datasets, query_group_by())

    return vals.assign(sources=sources)


def xr_to_dict_list(ds):
    for p in ds.sources.squeeze():
        time = pd.Timestamp(p.time.item())
        source = p.item()[0]  # Sources is many, but for now only care about the first
        yield {'time': time,
               'path': source.local_path}


def xr_filter_value(dataset, varname, value, dropdim='time'):
    return dataset.where(dataset[varname] == value).dropna(dropdim)

if __name__ == '__main__':
    main()

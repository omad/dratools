#!/g/data/v10/public/modules/agdc-py3-env/20161201/envs/agdc/bin/python
import sys

sys.path.append('/g/data/v10/public/modules/agdc-py3/1.1.17/lib/python3.5/site-packages')

from datacube import Datacube
import xarray as xr
import pandas as pd
import os

os.environ['GDAL_DATA'] = '/g/data/v10/public/modules/agdc-py3-env/20161201/envs/agdc/share/gdal'

dc = Datacube(config='/g/data/u46/users/dra547/damiencube.conf')


def add_wofs_meanings(df, column='wofs', prefix=''):
    df = df.copy()
    df[prefix + 'water'] = df[column] & 128 == 128
    df[prefix + 'cloud'] = df[column] & 64 == 64
    df[prefix + 'cloud_shadow'] = df[column] & 32 == 32
    df[prefix + 'high_slope'] = df[column] & 16 == 16
    df[prefix + 'terrain_shadow'] = df[column] & 8 == 8
    df[prefix + 'over_sea'] = df[column] & 4 == 4
    df[prefix + 'no_contiguity'] = df[column] & 2 == 2
    df[prefix + 'nodata'] = df[column] & 1 == 1
    df[prefix + 'dry'] = df[column] == 0
    return df


def load_new_wofs(lon, lat):
    data = dc.load(product='wofs_albers', longitude=lon, latitude=lat, crs='EPSG:4326', dask_chunks={'time': 1})

    df = data.to_dataframe()
    new = df.reset_index(level=['x', 'y'], drop=True)
    new = new.reset_index()
    new['date'] = new['time'].dt.date
    new = new.rename(columns={'water': 'wofs'})

    return add_wofs_meanings(new)


def load_old_wofs(lon, lat):
    old_wofs = xr.open_dataset(
        '/g/data/fk4/wofs/current/extents/145_-042/LS_WATER_145_-042_1987-08-24T23-24-34_2015-12-19T23-59-31.nc')

    old = old_wofs.sel(longitude=lon, latitude=lat, method='nearest').to_dataframe()
    old = old.drop(['crs', 'latitude', 'longitude'], axis=1)
    old = old.reset_index()
    old['date'] = old['time'].dt.date
    old = old.rename(columns={'Data': 'wofs'})
    return add_wofs_meanings(old)


def load_merged_wofs(lon, lat):
    old = load_old_wofs(lon, lat)
    new = load_new_wofs(lon, lat)
    merged = pd.merge(new, old, how='outer', on='date', suffixes=('_new', '_old')).set_index('date').sort_index()
    return merged


def main(lon, lat, filename):
    merged = load_merged_wofs(lon, lat)
    merged.to_csv(filename)


if __name__ == '__main__':
    if len(sys.argv) != 4:
        print('Usage: %s <lon> <lat> <output_csv_filename>' % sys.argv[0])
        exit()
    lon, lat = [float(arg) for arg in sys.argv[1:3]]
    filename = sys.argv[3]

    main(lon, lat, filename)


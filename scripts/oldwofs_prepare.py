# coding=utf-8
"""
Ingest data from the command-line.

python utils/bom_rainfall_prepare.py --output rainfall.yaml /g/data/rr5/agcd/0_05/rainfall/daily/*/*
"""
from __future__ import absolute_import

import uuid

import click
import netCDF4
import rasterio
import yaml
from datetime import datetime
import re
from tqdm import tqdm
from pathlib import Path


def prepare_datasets_netcdf(nc_file):
    image = netCDF4.Dataset(nc_file)
    times = image['time']

    projection = 'EPSG:4326'
    x, dx, _, y, _, dy = (float(n) for n in image['crs'].GeoTransform)

    left, right = x, x + dx * len(image['longitude'])
    bottom, top = y + dy * len(image['latitude']), y

    class CountableGenerator(object):
        def __len__(self):
            return len(times)

        def __iter__(self):
            for time in times:
                sensing_time = netCDF4.num2date(time, units=times.units, calendar=times.calendar).isoformat()
                yield {
                    'id': str(uuid.uuid4()),
                    'product_type': 'old_wofs',
                    'creation_dt': parse(image.date_created).isoformat(),
                    'platform': {'code': 'LANDSAT'},
                    'extent': {
                        'coord': {
                            'ul': {'lon': left, 'lat': top},
                            'ur': {'lon': right, 'lat': top},
                            'll': {'lon': left, 'lat': bottom},
                            'lr': {'lon': right, 'lat': bottom},
                        },
                        'from_dt': sensing_time,
                        'to_dt': sensing_time,
                        'center_dt': sensing_time
                    },
                    'format': {'name': 'NETCDF'},
                    'grid_spatial': {
                        'projection': {
                            'spatial_reference': projection,
                            'geo_ref_points': {
                                'ul': {'x': left, 'y': top},
                                'ur': {'x': right, 'y': top},
                                'll': {'x': left, 'y': bottom},
                                'lr': {'x': right, 'y': bottom},
                            },
                            # 'valid_data'
                        }
                    },
                    'image': {
                        'bands': {
                            'water': {
                                'path': str(Path(nc_file).absolute()),
                                'layer': 'Data',
                            }
                        }
                    },
                    'lineage': {'source_datasets': {}},
                }

    return CountableGenerator()


def prepare_datasets_geotiff(geotiff_file):
    with rasterio.open(geotiff_file) as image:
        file_path = Path(geotiff_file)

        projection = image.crs['init']

        left, bottom, right, top = image.bounds

        # Calc sensing time
        sensing_time = datetime(*[int(d)
                                  for d in re.split(r'[-T]',
                                                    re.findall(r'\d\d\d\d-[\d\-T]+', geotiff_file)[0])])
        creation_time = datetime.fromtimestamp(file_path.stat().st_ctime)

        return {
            'id': str(uuid.uuid4()),
            'product_type': 'old_wofs',
            'creation_dt': creation_time,
            'platform': {'code': 'LANDSAT'},
            'extent': {
                'coord': {
                    'ul': {'lon': left, 'lat': top},
                    'ur': {'lon': right, 'lat': top},
                    'll': {'lon': left, 'lat': bottom},
                    'lr': {'lon': right, 'lat': bottom},
                },
                'from_dt': sensing_time,
                'to_dt': sensing_time,
                'center_dt': sensing_time
            },
            'format': {'name': str(image.driver)},
            'grid_spatial': {
                'projection': {
                    'spatial_reference': projection,
                    'geo_ref_points': {
                        'ul': {'x': left, 'y': top},
                        'ur': {'x': right, 'y': top},
                        'll': {'x': left, 'y': bottom},
                        'lr': {'x': right, 'y': bottom},
                    },
                    # 'valid_data'
                }
            },
            'image': {
                'bands': {
                    'water': {
                        'path': str(file_path.absolute()),
                        'layer': '1',
                    }
                }
            },
            'lineage': {'source_datasets': {}},
        }


@click.command(help="Prepare old WOfS tiles for ingestion into the Data Cube.")
@click.argument('datasets',
                type=click.Path(exists=True, readable=True),
                nargs=-1)
@click.option('--output', help="Write datasets into this file",
              type=click.Path(exists=False, writable=True))
def main(datasets, output):
    with open(output, 'w') as stream:
        output_datasets = (prepare_datasets_geotiff(dataset)
                           for dataset in datasets)

        with click.progressbar(output_datasets,
                               length=len(datasets),
                               label='Loading datasets') as progress_bar_datasets:
            yaml.dump_all(progress_bar_datasets, stream)


if __name__ == "__main__":
    main()

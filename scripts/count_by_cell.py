import json

import click

from datacube.api import GridWorkflow
from datacube.ui import click as ui
from datacube.utils.geometry import CRS
from datacube.model import Range
# from datetime import datetime

# Setup for logging queries
# import logging
#
# logger = logging.getLogger()
# handler = logging.StreamHandler()
# formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
# handler.setFormatter(formatter)
# logger.addHandler(handler)
# logger.setLevel(logging.DEBUG)
#
# logging.getLogger('sqlalchemy.engine').setLevel('INFO')


# dc = datacube.Datacube(app='shapes.ipynb')
# gw = datacube.api.GridWorkflow(product='ls8_nbar_albers', index=dc.index)
#
# def plot_cell_count(cells):
#     x = sorted(set(v[0] for v in cells.keys()))
#     y = sorted(set(v[1] for v in cells.keys()), reverse=True)
#     data = xr.DataArray(np.zeros((len(y), len(x)), dtype=int), dims=['y', 'x'], coords=dict(x=x, y=y))
#     for cell_index, tile in cells.items():
#         data.loc[cell_index[1], cell_index[0]] = tile.sources.shape[0]
#     data.plot()
#
# solar_day_cells_2015 = gw.list_cells(product='ls8_nbar_albers', time=('2015', '2016'), group_by='solar_day')
# plot_cell_count(solar_day_cells_2015)

# def map_expression_type(name, expr):
#     if isinstance(expr, Range):
#         if name == 'time':
#             import pdb; pdb.set_trace()
#             return tuple([str(int(el)) for el in expr])
#         else:
#             return tuple(list(expr))
#     else:
#         return expr


@click.command()
@ui.global_cli_options
@click.argument('filename')
@click.argument('product')
@ui.parsed_search_expressions
@ui.pass_index('cell-count')
def main(index, filename, product, expressions):
    """
    For the given search expression, count how many datasets exist in each product cell,
    saving the output as GeoJSON.
    """
    # expressions = {k: map_expression_type(k, v) for k, v in expressions.items()}
    # import pdb; pdb.set_trace()
    save_grid_count_to_file(filename, index=index, product=product, **expressions)


def save_grid_count_to_file(filename, index, **queryargs):
    gw = GridWorkflow(product=queryargs['product'], index=index)

    cells = gw.list_cells(group_by='solar_day', **queryargs)

    geojson = cells_list_to_featurecollection(cells)

    with open(filename, 'w') as dest:
        json.dump(geojson, dest)


def cells_list_to_featurecollection(cells_dict):
    return {'type': 'FeatureCollection',
            'features': [tile_to_geojsonfeature(tile, cell=cell_to_str(cell))
                         for cell, tile in cells_dict.items()]}


def tile_to_geojsonfeature(tile, **props):
    geometry = tile.geobox.extent.to_crs(CRS('EPSG:4326')).__geo_interface__
    feature = {'type': 'Feature',
               'geometry': geometry,
               'properties': dict(count=len(tile.sources),
                                  **props)}
    return feature


def cell_to_str(cell):
    return ', '.join(str(el) for el in cell)


if __name__ == '__main__':
    main()

# 3.5 minutes for 2 years



import fiona
import shapely.ops
from shapely.geometry import shape, mapping
from datacube.utils.geometry import Geometry
from datacube.model import CRS
import sys
from datacube import Datacube

product_name = sys.argv[1]
shapefile = sys.argv[2]


with fiona.open(shapefile) as input_region:
    joined = shapely.ops.unary_union(list(shape(geom['geometry']) for geom in input_region))
    final = joined.convex_hull
    crs = CRS(input_region.crs_wkt)
    boundary_polygon = Geometry(mapping(final), crs)

dc = Datacube()
product = dc.index.products.get_by_name(product_name)

query_tiles = set(
    tile_index for tile_index, tile_geobox in
    product.grid_spec.tiles_inside_geopolygon(boundary_polygon))

print(query_tiles)

# for tile_index, _ in product.grid_spec.tiles_inside_geopolygon(boundary_polygon):
#     print(tile_index)

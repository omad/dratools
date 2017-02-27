import datacube
from datacube.storage.storage import write_dataset_to_netcdf
from datacube.storage.masking import mask_valid_data as mask_invalid_data, make_mask
from datacube.helpers import ga_pq_fuser
import fiona

dc = datacube.Datacube(app='img_retrieval')

vec_file = '/home/554/msi554/ERF_fieldsite_area_buffer.shp'
acq_min = '2013-07'
acq_max = '2013-09'
product_type = 'nbar'
if product_type in ['nbar', 'nbart']:
    measurements_list = ['blue', 'green', 'red', 'nir', 'swir1', 'swir2']

platform_list = ['ls8']

with fiona.open(vec_file, 'r') as src:
    lon_range = (src.bounds[0], src.bounds[2])
    lat_range = (src.bounds[-1], src.bounds[1])
    crs = str(src.crs_wkt)
print(lon_range, lat_range)
print(crs)

for platform in platform_list:
    product_name = '{}_{}_albers'.format(platform, product_type)
    print('Loading product: {}'.format(product_name))
    output_file = '/g/data/u46/users/dra547/erf_07_09_2013_' + product_name + '.cdf'
    print(output_file)

    dataset = dc.load(product=product_name,
                      x=lon_range, y=lat_range,
                      time=(acq_min, acq_max),
                      group_by='solar_day',
                      crs=crs, measurements=measurements_list)
    # Load PQ Mask
    mask_product = '{}_{}_albers'.format(platform, 'pq')
    sensor_pq = dc.load(product=mask_product, group_by='solar_day', fuse_func=ga_pq_fuser, like=dataset)
    cloud_free = make_mask(sensor_pq.pixelquality, ga_good_pixel=True)

    dataset = dataset.where(cloud_free).fillna(-999).astype('int16')
    dataset.attrs['crs'] = sensor_pq.crs # Temporarily required until xarray issue #1009 gets into a release

    print(dataset)
    write_dataset_to_netcdf(dataset, output_file)

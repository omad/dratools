
datacube dataset search product=ls5_nbar_albers '1996-01-01 < time < 1996-01-02'
id: d47d927e-716f-48fc-bf1f-7aba28f37cf9
product: ls5_nbar_albers
status: active
locations:
- file:///g/data/rs0/datacube/002/LS5_TM_NBAR/10_-35/LS5_TM_NBAR_3577_10_-35_19960101232243500000.nc
fields:
    format: NetCDF
    instrument: TM
    lat: {begin: -31.74001178621786, end: -30.788614779327567}
    lon: {begin: 142.57758955084404, end: 143.72479117031412}
    platform: LANDSAT_5
    product_type: nbar
    time: {begin: '1996-01-01T23:22:43.500000', end: '1996-01-01T23:22:43.500000'}
---
id: 7cabd43a-20c8-4531-8ca8-23dd90779333
product: ls5_nbar_albers
status: active
locations:
- file:///g/data/rs0/datacube/002/LS5_TM_NBAR/15_-21/LS5_TM_NBAR_3577_15_-21_19960101231844500000.nc
fields:
    format: NetCDF
    instrument: TM
    lat: {begin: -18.392326704802237, end: -17.846328960585353}
    lon: {begin: 146.18696311557267, end: 147.17934013616025}
    platform: LANDSAT_5
    product_type: nbar
    time: {begin: '1996-01-01T23:18:44.500000', end: '1996-01-01T23:18:44.500000'}
---
id: 8fec16a3-bbbd-42a1-83a0-c8fd7dc1cbcd
product: ls5_nbar_albers
status: active
locations:
- file:///g/data/rs0/datacube/002/LS5_TM_NBAR/16_-20/LS5_TM_NBAR_3577_16_-20_19960101231844500000.nc
fields:
    format: NetCDF
    instrument: TM
    lat: {begin: -17.846328960585353, end: -16.902508327474667}
    lon: {begin: 147.0136485360093, end: 147.51664494516416}
    platform: LANDSAT_5
    product_type: nbar
    time: {begin: '1996-01-01T23:18:44.500000', end: '1996-01-01T23:18:44.500000'}


$ datacube dataset info 8fec16a3-bbbd-42a1-83a0-c8fd7dc1cbcd --show-sources

$ datacube metadata_type list
MetadataType(name='eo', id_=1)
MetadataType(name='landsat_l1_scene', id_=4)
MetadataType(name='landsat_scene', id_=3)
MetadataType(name='telemetry', id_=2)



$ datacube metadata_type show -v eo
Earth Observation datasets.
#
Type of datasets produced by the eodatasets library.
(or of similar structure)
#
https://github.com/GeoscienceAustralia/eo-datasets
#
Search fields: dataset_type_id, gsi, id, instrument, lat, lon, metadata_doc, metadata_type, metadata_type_id, orbit, platform, product, product_type, sat_path, sat_row, time, uri
{'dataset': {'creation_dt': ['creation_dt'],
             'format': ['format', 'name'],
             'grid_spatial': ['grid_spatial', 'projection'],
             'id': ['id'],
             'label': ['ga_label'],
             'measurements': ['image', 'bands'],
             'search_fields': {'gsi': {'description': 'Ground Station Identifier (eg. ASA)',
#
                                       'offset': ['acquisition', 'groundstation', 'code']},
                               'instrument': {'description': 'Instrument name',
                                              'offset': ['instrument', 'name']},
                               'lat': {'description': 'Latitude range',
                                       'max_offset': [['extent', 'coord', 'ur', 'lat'],
                                                      ['extent', 'coord', 'lr', 'lat'],
                                                      ['extent', 'coord', 'ul', 'lat'],
                                                      ['extent', 'coord', 'll', 'lat']],
                                       'min_offset': [['extent', 'coord', 'ur', 'lat'],
                                                      ['extent', 'coord', 'lr', 'lat'],
                                                      ['extent', 'coord', 'ul', 'lat'],
                                                      ['extent', 'coord', 'll', 'lat']],
                                       'type': 'double-range'},
                               'lon': {'description': 'Longitude range',
                                       'max_offset': [['extent', 'coord', 'ul', 'lon'],
                                                      ['extent', 'coord', 'ur', 'lon'],
                                                      ['extent', 'coord', 'll', 'lon'],
                                                      ['extent', 'coord', 'lr', 'lon']],
                                       'min_offset': [['extent', 'coord', 'ul', 'lon'],
                                                      ['extent', 'coord', 'ur', 'lon'],
                                                      ['extent', 'coord', 'll', 'lon'],
                                                      ['extent', 'coord', 'lr', 'lon']],
                                       'type': 'double-range'},
                               'orbit': {'description': 'Orbit number',
                                         'offset': ['acquisition', 'platform_orbit'],
                                         'type': 'integer'},
                               'platform': {'description': 'Platform code',
                                            'offset': ['platform', 'code']},
                               'product_type': {'description': 'Product code',
                                                'offset': ['product_type']},
                               'sat_path': {'description': 'Landsat path',
                                            'max_offset': [['image',
                                                            'satellite_ref_point_end',
                                                            'x'],
                                                           ['image',
                                                            'satellite_ref_point_start',
                                                            'x']],
                                            'min_offset': [['image',
                                                            'satellite_ref_point_start',
                                                            'x']],
                                            'type': 'integer-range'},
                               'sat_row': {'description': 'Landsat row',
                                           'max_offset': [['image', 'satellite_ref_point_end', 'y'],
                                                          ['image',
                                                           'satellite_ref_point_start',
                                                           'y']],
                                           'min_offset': [['image',
                                                           'satellite_ref_point_start',
                                                           'y']],
                                           'type': 'integer-range'},
                               'time': {'description': 'Acquisition time',
                                        'max_offset': [['extent', 'to_dt'],
                                                       ['extent', 'center_dt']],
                                        'min_offset': [['extent', 'from_dt'],
                                                       ['extent', 'center_dt']],
                                        'type': 'datetime-range'}},
             'sources': ['lineage', 'source_datasets']},
 'description': 'Earth Observation datasets.\n'
                '\n'
                'Type of datasets produced by the eodatasets library.\n'
                '(or of similar structure)\n'
                '\n'
                'https://github.com/GeoscienceAustralia/eo-datasets\n',
 'name': 'eo'}


$ datacube product list
   name                          description                                        product_type              instrument              format             platform
id
36            bom_rainfall_grids  Interpolated Rain Gauge Precipitation 1-Day Au...                  rainfall              rain gauge             NETCDF                      BoM
32                      dsm1sv10                               DSM 1sec Version 1.0                       DEM                     SIR               ENVI                     SRTM
53                     gamma_ray  The 2015 radiometric or gamma-ray grid of Aust...                 gamma_ray  gamma_ray spectrometer             NETCDF                 aircraft
42                 ls5_fc_albers  Landsat 5 Fractional Cover 25 metre, 100km til...          fractional_cover                      TM             NetCDF                LANDSAT_5
2               ls5_level1_scene      Landsat 5 Level 1 At-sensor Radiance 25 metre                    level1                      TM            GeoTiff                LANDSAT_5
6                ls5_nbar_albers  Landsat 5 Surface Reflectance NBAR 25 metre, 1...                      nbar                      TM             NetCDF                LANDSAT_5
3                 ls5_nbar_scene                            Landsat 5 NBAR 25 metre                      nbar                      TM            GeoTiff                LANDSAT_5
26              ls5_nbart_albers  Landsat 5 Surface Reflectance NBART 25 metre, ...                     nbart                      TM             NetCDF                LANDSAT_5
4                ls5_nbart_scene                           Landsat 5 NBART 25 metre                     nbart                      TM            GeoTiff                LANDSAT_5
41               ls5_ndvi_albers  Landsat 5 Normalised Difference Vegetation Ind...                      ndvi                      TM             NetCDF                LANDSAT_5
23                 ls5_pq_albers  Landsat 5 Pixel Quality 25 metre, 100km tile, ...                       pqa                      TM             NetCDF                LANDSAT_5
5                   ls5_pq_scene                              Landsat 5 PQ 25 metre                       pqa                      TM            GeoTiff                LANDSAT_5
1   ls5_satellite_telemetry_data                 Landsat 5 Satellite Telemetry Data  satellite_telemetry_data                      TM                NaN                LANDSAT_5
44                 ls7_fc_albers  Landsat 7 Fractional Cover 25 metre, 100km til...          fractional_cover                     ETM             NetCDF                LANDSAT_7
9               ls7_level1_scene      Landsat 7 Level 1 At-sensor Radiance 25 metre                    level1                     ETM            GeoTiff                LANDSAT_7
21               ls7_nbar_albers  Landsat 7 Surface Reflectance NBAR 25 metre, 1...                      nbar                     ETM             NetCDF                LANDSAT_7
10                ls7_nbar_scene                            Landsat 7 NBAR 25 metre                      nbar                     ETM            GeoTiff                LANDSAT_7
29              ls7_nbart_albers  Landsat 7 Surface Reflectance NBART 25 metre, ...                     nbart                     ETM             NetCDF                LANDSAT_7
11               ls7_nbart_scene                           Landsat 7 NBART 25 metre                     nbart                     ETM            GeoTiff                LANDSAT_7
45               ls7_ndvi_albers  Landsat 7 Normalised Difference Vegetation Ind...                      ndvi                     ETM             NetCDF                LANDSAT_7
22                 ls7_pq_albers  Landsat 7 Pixel Quality 25 metre, 100km tile, ...                       pqa                     ETM             NetCDF                LANDSAT_7
12                  ls7_pq_scene                              Landsat 7 PQ 25 metre                       pqa                     ETM            GeoTiff                LANDSAT_7
8   ls7_satellite_telemetry_data                 Landsat 7 Satellite Telemetry Data  satellite_telemetry_data                     ETM                NaN                LANDSAT_7
47                 ls8_fc_albers  Landsat 8 Fractional Cover 25 metre, 100km til...          fractional_cover                OLI_TIRS             NetCDF                LANDSAT_8
40          ls8_level1_oli_scene  Landsat 8 OLI Level 1 At-sensor Radiance 25 metre                    level1                     OLI            GeoTiff                LANDSAT_8
14              ls8_level1_scene  Landsat 8 Level 1 OLI-TIRS At-sensor Radiance ...                    level1                OLI_TIRS            GeoTiff                LANDSAT_8
19               ls8_nbar_albers  Landsat 8 Surface Reflectance NBAR 25 metre, 1...                      nbar                OLI_TIRS             NetCDF                LANDSAT_8
60           ls8_nbar_oli_albers  Landsat 8 Surface Reflectance NBAR 25 metre, 1...                      nbar                     OLI             NetCDF                LANDSAT_8
57            ls8_nbar_oli_scene                        Landsat 8 OLI NBAR 25 metre                      nbar                     OLI            GeoTiff                LANDSAT_8
15                ls8_nbar_scene                            Landsat 8 NBAR 25 metre                      nbar                OLI_TIRS            GeoTiff                LANDSAT_8
28              ls8_nbart_albers  Landsat 8 Surface Relfectance NBART 25 metre, ...                     nbart                OLI_TIRS             NetCDF                LANDSAT_8
61          ls8_nbart_oli_albers  Landsat 8 Surface Relfectance NBART 25 metre, ...                     nbart                     OLI             NetCDF                LANDSAT_8
58           ls8_nbart_oli_scene                       Landsat 8 OLI NBART 25 metre                     nbart                     OLI            GeoTiff                LANDSAT_8
16               ls8_nbart_scene                           Landsat 8 NBART 25 metre                     nbart                OLI_TIRS            GeoTiff                LANDSAT_8
55               ls8_ndvi_albers  Landsat 8 Normalised Difference Vegetation Ind...                      ndvi                OLI_TIRS             NetCDF                LANDSAT_8
20                 ls8_pq_albers  Landsat 8 Pixel Quality 25 metre, 100km tile, ...                       pqa                OLI_TIRS             NetCDF                LANDSAT_8
59              ls8_pq_oli_scene                          Landsat 8 OLI PQ 25 metre                       pqa                     OLI            GeoTiff                LANDSAT_8
17                  ls8_pq_scene                              Landsat 8 PQ 25 metre                       pqa                OLI_TIRS            GeoTiff                LANDSAT_8
13  ls8_satellite_telemetry_data                 Landsat 8 Satellite Telemetry Data  satellite_telemetry_data                    None                NaN                LANDSAT_8
49            modis_mcd43a1_tile             MODIS 500 metre MCD43A1 Collection 006                   MCD43A1                   MODIS  HDF4_EOS:EOS_GRID               AQUA_TERRA
50            modis_mcd43a2_tile             MODIS 500 metre MCD43A2 Collection 006                   MCD43A2                   MODIS  HDF4_EOS:EOS_GRID               AQUA_TERRA
51            modis_mcd43a3_tile             MODIS 500 metre MCD43A3 Collection 006                   MCD43A3                   MODIS  HDF4_EOS:EOS_GRID               AQUA_TERRA
52            modis_mcd43a4_tile             MODIS 500 metre MCD43A4 Collection 006                   MCD43A4                   MODIS  HDF4_EOS:EOS_GRID               AQUA_TERRA
56                srtm_dem1sv1_0                               DEM 1sec Version 1.0                       DEM                     SIR                AIG  Space Shuttle Endeavour
46                   wofs_albers  Historic Flood Mapping Water Observations from...                      wofs                    None             NetCDF                     None


$ datacube product show ls5_nbar_albers
**JSON OUTPUT**

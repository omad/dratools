
from datacube import Datacube
from datacube.api import GridWorkflow
import logging

logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter(
        '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

logging.getLogger('sqlalchemy.engine').setLevel('INFO')
logger.debug('starting count.')

dc = Datacube()

# print(dc.list_products())


product = 'ls7_fc_albers'


gw = GridWorkflow(index=dc.index, product=product)

foo = gw.cell_observations(time=('1999-01-01', '2001-01-01'), product=product)

for k, v in foo.items():
    print(k, len(v['datasets'])) # v dict also contains 'geobox'


logger.debug('counting done.')


# 3.5 minutes for 2 years
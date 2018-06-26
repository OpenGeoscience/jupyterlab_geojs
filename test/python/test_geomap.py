import logging
import unittest

logging.basicConfig(level=logging.DEBUG)

from . import utils
from jupyterlab_geojs import GeoJSMap


class TestGeoMap(unittest.TestCase):

    def test_basic_model(self):
        '''Test creating simple map with osm and feature layer'''
        geo_map = GeoJSMap(zoom=10)  # pass in option to constructor
        geo_map.center = {'x': -73, 'y': 42.5}  # set option as public member
        osm_layer = geo_map.createLayer('osm')
        feature_layer = geo_map.createLayer('feature')
        data = geo_map._build_data()
        #print(data)

        utils.validate_model(data)

        self.assertIsInstance(data, dict)
        self.assertTrue('options' in data)
        self.assertTrue('layers' in data)

        utils.write_model(data, 'basic_model.json')

if __name__ == '__main__':
    unittest.main()

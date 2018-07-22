import logging
import unittest

logging.basicConfig(level=logging.DEBUG)

from . import utils
from jupyterlab_geojs import Scene


class TestGeoMap(unittest.TestCase):

    def test_basic_model(self):
        '''Test creating simple map with osm and feature layer'''
        scene = Scene(zoom=10)  # pass in option to constructor
        scene.center = {'x': -73, 'y': 42.5}  # set option as public member
        osm_layer = scene.createLayer('osm')
        feature_layer = scene.createLayer('feature')
        data = scene._build_data()
        #print(data)

        utils.validate_model(data)

        self.assertIsInstance(data, dict)
        self.assertTrue('options' in data)
        self.assertTrue('layers' in data)

        utils.write_model(data, 'basic_model.json')

if __name__ == '__main__':
    unittest.main()

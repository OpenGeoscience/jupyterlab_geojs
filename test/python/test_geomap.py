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
        osm_layer = scene.create_layer('osm')
        feature_layer = scene.create_layer('feature')
        display_model = scene._build_display_model()
        #print(display_model)

        utils.validate_model(display_model)

        self.assertIsInstance(display_model, dict)
        self.assertTrue('options' in display_model)
        self.assertTrue('layers' in display_model)

        utils.write_model(display_model, 'basic_model.json')

if __name__ == '__main__':
    unittest.main()

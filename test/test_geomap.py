import logging
import os
import sys
import unittest

logging.basicConfig(level=logging.DEBUG)

from jupyterlab_geojs import GeoJSMap


class TestGeoMap(unittest.TestCase):

    def test_create(self):
        """Test creating OSM layer"""
        #print('shortDescription():', self.shortDescription())
        geo_map = GeoJSMap()
        osm_layer = geo_map.createLayer('osm')
        data = geo_map._build_data()
        print(data)
        self.assertIsInstance(data, dict)
        self.assertTrue('options' in data)
        self.assertTrue('layers' in data)

if __name__ == '__main__':
    unittest.main()

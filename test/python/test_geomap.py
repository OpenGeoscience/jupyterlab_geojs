import json
import logging
import os
import sys
import unittest

import jsonschema

logging.basicConfig(level=logging.DEBUG)

from jupyterlab_geojs import GeoJSMap


class TestGeoMap(unittest.TestCase):

    def test_create(self):
        """Test creating OSM layer"""
        #print('shortDescription():', self.shortDescription())
        geo_map = GeoJSMap()
        osm_layer = geo_map.createLayer('osm')
        feature_layer = geo_map.createLayer('feature')
        data = geo_map._build_data()
        print(data)
        self.assertIsInstance(data, dict)
        self.assertTrue('options' in data)
        self.assertTrue('layers' in data)

        source_dir = os.path.abspath(os.path.dirname(__file__))
        schema_filename = os.path.join(source_dir, os.pardir, os.pardir, 'model', 'model.schema.json')
        schema = None
        with open(schema_filename) as f:
            schema_string = f.read()
        schema = json.loads(schema_string)
        print('validating against schema:')
        jsonschema.validate(data, schema)

if __name__ == '__main__':
    unittest.main()

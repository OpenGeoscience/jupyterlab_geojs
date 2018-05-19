import json
import logging
import os
import sys
import unittest

import jsonschema

logging.basicConfig(level=logging.DEBUG)

from jupyterlab_geojs import GeoJSMap


class TestGeoMap(unittest.TestCase):

    def test_basic_model(self):
        '''Test creating simple map with osm and feature layer'''
        geo_map = GeoJSMap(zoom=10)  # pass in option to constructor
        geo_map.center = {'x': -73, 'y': 42.5}  # set option as public member
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

        # Optionally write result to model file
        model_filename = os.path.join(source_dir, os.pardir, 'models', 'basic_model.json')
        data_string = json.dumps(data)
        with open(model_filename, 'w') as f:
            f.write(data_string)
            print('Wrote {}'.format(model_filename))

if __name__ == '__main__':
    unittest.main()

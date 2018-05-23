import json
import logging
import os
import sys
import unittest

import jsonschema

logging.basicConfig(level=logging.DEBUG)

from jupyterlab_geojs import GeoJSMap


class TestBasicFeatures(unittest.TestCase):

    def test_quad_feature(self):
        '''Test creating simple map with osm and feature layer'''
        geo_map = GeoJSMap(zoom=10)  # pass in option to constructor
        geo_map.center = {'x': -97.67, 'y': 31.80}  # set option as public member
        geo_map.zoom = 4
        osm_layer = geo_map.createLayer('osm')
        feature_layer = geo_map.createLayer('feature')

        # Point data
        cities = [
            {'lon': -74.0059413, 'lat': 40.7127837, 'name': "New York", 'population': 8405837},
            {'lon': -118.2436849, 'lat': 34.0522342, 'name': "Los Angeles", 'population': 3884307},
            {'lon': -87.6297982, 'lat': 41.8781136, 'name': "Chicago", 'population': 2718782},
            {'lon': -95.3698028, 'lat': 29.7604267, 'name': "Houston", 'population': 2195914},
            {'lon': -75.1652215, 'lat': 39.9525839, 'name': "Philadelphia", 'population': 1553165},
            {'lon': -112.0740373, 'lat': 33.4483771, 'name': "Phoenix", 'population': 1513367}
        ]
        positions = [{'x':city['lon'], 'y':city['lat']} for city in cities]
        style = {'fillColor': 'red', 'strokeColor': 'black', 'strokeWidget': 2}
        feature_layer.createFeature('point', data=cities, position=positions, style=style)

        # Quad data
        quad = feature_layer.createFeature('quad')
        quad.data = [{
            # Copied from http://opengeoscience.github.io/geojs/tutorials/video_on_map/
            'ul': {'x': -129.0625, 'y': 42.13468456089552},
            'lr': {'x': -100.9375, 'y': 29.348416310781797}
        }]
        quad.style = {
            'color': 'magenta',
            'opacity': 0.2
        }

        # Build data model
        data = geo_map._build_data()
        print(data)

        # Validate data model against schema
        source_dir = os.path.abspath(os.path.dirname(__file__))
        schema_filename = os.path.join(source_dir, os.pardir, os.pardir, 'model', 'model.schema.json')
        schema = None
        with open(schema_filename) as f:
            schema_string = f.read()
        schema = json.loads(schema_string)
        print('validating against schema:')
        jsonschema.validate(data, schema)

        # Optionally write result to model file
        model_filename = os.path.join(source_dir, os.pardir, 'models', 'basic_features.json')
        data_string = json.dumps(data)
        #data_string = json.dumps(data, sort_keys=True, indent=2)
        with open(model_filename, 'w') as f:
            f.write(data_string)
            print('Wrote {}'.format(model_filename))

if __name__ == '__main__':
    unittest.main()

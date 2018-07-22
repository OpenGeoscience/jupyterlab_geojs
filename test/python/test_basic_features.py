import logging
import unittest

logging.basicConfig(level=logging.DEBUG)

from . import utils
from jupyterlab_geojs import Scene


class TestBasicFeatures(unittest.TestCase):

    def test_quad_feature(self):
        '''Test creating simple map with osm and feature layer'''
        scene = Scene(zoom=10)  # pass in option to constructor
        scene.center = {'x': -97.67, 'y': 31.80}  # set option as public member
        scene.zoom = 4
        osm_layer = scene.create_layer('osm')
        feature_layer = scene.create_layer('feature', features=['point', 'quad'])

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
        style = {'strokeColor': 'black', 'strokeWidth': 2, 'radius': 12}
        point_feature = feature_layer.create_feature(
            'point', cities, position=positions, style=style)
        point_feature.enableTooltip = True  # adds ui layer in JS but NOT in python
        point_feature.colormap = {
            'colorseries': 'rainbow',
            'field': 'lon',
            'range': [-118.2436849, -74.0059413]
        }

        # Quad data
        feature_data = [{
            # Copied from http://opengeoscience.github.io/geojs/tutorials/video_on_map/
            'ul': {'x': -129.0625, 'y': 42.13468456089552},
            'lr': {'x': -100.9375, 'y': 29.348416310781797}
        }]
        quad = feature_layer.create_feature('quad', feature_data)
        quad.style = {
            'color': 'magenta',
            'opacity': 0.2
        }

        # Build data model
        data = scene._build_data()
        print(data)

        # Validate data model against schema
        utils.validate_model(data)

        # Optionally write result to model file
        utils.write_model(data, 'basic-features_model.json')

if __name__ == '__main__':
    unittest.main()

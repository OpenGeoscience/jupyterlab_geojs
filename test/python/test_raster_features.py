import os
import unittest

from . import utils
from jupyterlab_geojs import GeoJSMap


class TestRasterFeatures(unittest.TestCase):

    def test_rgb_image(self):
        '''Test creating raster feature'''
        filename = os.path.join(utils.data_folder, 'rasterwithpalette.tif')

        geo_map = GeoJSMap()
        geo_map.center = {'x': -76.5, 'y': 43.0};
        geo_map.zoom = 7;
        geo_map.createLayer('osm');
        feature_layer = geo_map.createLayer('feature', features=['quad.image'])
        quad = feature_layer.createFeature('raster', filename=filename)
        quad.style = {
            'opacity': 0.5
        }

        data = geo_map._build_data()
        #print(data)

        utils.validate_model(data)
        utils.write_model(data, 'raster_rgb.json')

    def test_utm_image(self):
        filename = os.path.join(utils.data_folder, 'utm.tif')

        geo_map = GeoJSMap()
        geo_map.center = {'x': -74.5, 'y': 6.0};
        geo_map.zoom = 10;
        geo_map.createLayer('osm');
        feature_layer = geo_map.createLayer('feature', features=['quad.image'])
        quad = feature_layer.createFeature('raster', filename=filename)
        quad.style = {
            'opacity': 0.8
        }

        data = geo_map._build_data()
        #print(data)

        # Write model (don't need to validate again)
        utils.write_model(data, 'raster_utm.json')

if __name__ == '__main__':
    unittest.main()

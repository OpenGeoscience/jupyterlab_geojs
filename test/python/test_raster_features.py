import os
import unittest

from . import utils
from jupyterlab_geojs import Scene


class TestRasterFeatures(unittest.TestCase):

    def test_rgb_image(self):
        '''Test creating raster feature'''
        filename = os.path.join(utils.data_folder, 'rasterwithpalette.tif')

        scene = Scene()
        # scene.center = {'x': -76.5, 'y': 43.0};
        # scene.zoom = 7;
        scene.create_layer('osm');
        feature_layer = scene.create_layer('feature', features=['quad.image'])
        quad = feature_layer.create_feature('raster', filename=filename)
        quad.style = {
            'opacity': 0.5
        }

        corners = quad.get_corner_points()
        scene.set_zoom_and_center(corners=corners)

        data = scene._build_data()
        #print(data)

        utils.validate_model(data)
        utils.write_model(data, 'raster-rgb_model.json')

    def test_utm_image(self):
        filename = os.path.join(utils.data_folder, 'utm.tif')

        scene = Scene()
        scene.center = {'x': -74.5, 'y': 6.0};
        scene.zoom = 10;
        scene.create_layer('osm');
        feature_layer = scene.create_layer('feature', features=['quad.image'])
        quad = feature_layer.create_feature('raster', filename=filename)
        quad.style = {
            'opacity': 0.8
        }

        data = scene._build_data()
        #print(data)

        # Write model (don't need to validate again)
        utils.write_model(data, 'raster-utm_model.json')

if __name__ == '__main__':
    unittest.main()

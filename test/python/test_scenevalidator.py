import logging
import os
import unittest

from . import utils

logging.basicConfig(level=logging.DEBUG)

from jupyterlab_geojs import GeoJSMap


class TestSceneValidator(unittest.TestCase):

    def test_pointcloud_osm(self):
        '''pointcloud cannot be used in scene with osm layer'''
        scene = GeoJSMap()
        scene.createLayer('osm')
        feature_layer = scene.createLayer('feature')
        filename = os.path.join(utils.data_folder, '100-points.las')
        #feature_layer.createFeature('pointcloud', filename=filename)
        self.assertRaises(Exception, feature_layer.createFeature, 'pointcloud', filename=filename)

    def test_osm_pointcloud(self):
        '''osm layer cannot be added to scene with pointcloud feature'''
        scene = GeoJSMap()
        feature_layer = scene.createLayer('feature')
        filename = os.path.join(utils.data_folder, '100-points.las')
        feature_layer.createFeature('pointcloud', filename=filename)
        self.assertRaises(Exception, scene.createLayer, 'osm')

    def test_pointcloud_point(self):
        '''pointcloud cannot be used in scene with point feature'''
        scene = GeoJSMap()
        feature_layer = scene.createLayer('feature')
        feature_layer.createFeature('point')
        filename = os.path.join(utils.data_folder, '100-points.las')
        #feature_layer.createFeature('pointcloud', filename=filename)
        self.assertRaises(
            Exception, feature_layer.createFeature, 'pointcloud', filename=filename)

    def test_point_pointcloud(self):
        '''pointcloud feature cannot be added to scene with point feature'''
        scene = GeoJSMap()
        feature_layer = scene.createLayer('feature')
        filename = os.path.join(utils.data_folder, '100-points.las')
        feature_layer.createFeature('pointcloud', filename=filename)
        #feature_layer.createFeature('point')
        self.assertRaises(Exception, feature_layer.createFeature, 'point')

    def test_pointcloud_pointcloud(self):
        '''only one pointcloud feature cannot be added to scene'''
        scene = GeoJSMap()
        feature_layer = scene.createLayer('feature')
        filename = os.path.join(utils.data_folder, '100-points.las')
        feature_layer.createFeature('pointcloud', filename=filename)

        #feature_layer.createFeature('pointcloud', filename=filename)
        self.assertRaises(
            Exception, feature_layer.createFeature, 'pointcloud', filename=filename)


if __name__ == '__main__':
    unittest.main()

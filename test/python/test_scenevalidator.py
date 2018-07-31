import logging
import os
import unittest

from . import utils

logging.basicConfig(level=logging.DEBUG)

from jupyterlab_geojs import Scene


class TestSceneValidator(unittest.TestCase):

    def test_pointcloud_osm(self):
        '''pointcloud cannot be used in scene with osm layer'''
        scene = Scene()
        scene.create_layer('osm')
        feature_layer = scene.create_layer('feature')
        filename = os.path.join(utils.data_folder, '100-points.las')
        #feature_layer.create_feature('pointcloud', data=filename)
        self.assertRaises(Exception, feature_layer.create_feature, 'pointcloud', data=filename)

    def test_osm_pointcloud(self):
        '''osm layer cannot be added to scene with pointcloud feature'''
        scene = Scene()
        feature_layer = scene.create_layer('feature')
        filename = os.path.join(utils.data_folder, '100-points.las')
        feature_layer.create_feature('pointcloud', data=filename)
        self.assertRaises(Exception, scene.create_layer, 'osm')

    def test_pointcloud_point(self):
        '''pointcloud cannot be used in scene with point feature'''
        scene = Scene()
        feature_layer = scene.create_layer('feature')
        feature_layer.create_feature('point', data=[])
        filename = os.path.join(utils.data_folder, '100-points.las')
        #feature_layer.create_feature('pointcloud', data=filename)
        self.assertRaises(
            Exception, feature_layer.create_feature, 'pointcloud', data=filename)

    def test_point_pointcloud(self):
        '''pointcloud feature cannot be added to scene with point feature'''
        scene = Scene()
        feature_layer = scene.create_layer('feature')
        filename = os.path.join(utils.data_folder, '100-points.las')
        feature_layer.create_feature('pointcloud', data=filename)
        #feature_layer.create_feature('point')
        self.assertRaises(Exception, feature_layer.create_feature, 'point', data=[])

    def test_pointcloud_pointcloud(self):
        '''only one pointcloud feature cannot be added to scene'''
        scene = Scene()
        feature_layer = scene.create_layer('feature')
        filename = os.path.join(utils.data_folder, '100-points.las')
        feature_layer.create_feature('pointcloud', data=filename)

        #feature_layer.create_feature('pointcloud', data=filename)
        self.assertRaises(
            Exception, feature_layer.create_feature, 'pointcloud', data=filename)


if __name__ == '__main__':
    unittest.main()

import os
import unittest

from . import utils
from jupyterlab_geojs import GeoJSMap


class TestPointCloudFeatures(unittest.TestCase):

    def test_las(self):
        '''Test creating pointcloud feature'''
        filename = os.path.join(utils.data_folder, '100-points.las')

        geo_map = GeoJSMap()
        # geo_map.center = {'x': -76.5, 'y': 43.0};
        # geo_map.zoom = 7;
        # geo_map.createLayer('osm');
        feature_layer = geo_map.createLayer('feature')
        pointcloud = feature_layer.createFeature('pointcloud', filename=filename)

        data = geo_map._build_data()
        #print(data)

        utils.validate_model(data)
        utils.write_model(data, 'pointcloud_100.json')

if __name__ == '__main__':
    unittest.main()

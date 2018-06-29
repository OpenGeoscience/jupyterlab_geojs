import os
import unittest

from . import utils
from jupyterlab_geojs import GeoJSMap


class TestPointCloudFeatures(unittest.TestCase):

    def test_las(self):
        '''Test creating pointcloud feature'''
        filename = os.path.join(utils.data_folder, '100-points.las')

        geo_map = GeoJSMap()
        feature_layer = geo_map.createLayer('feature')
        pointcloud = feature_layer.createFeature('pointcloud', filename=filename)
        data = geo_map._build_data()

        #utils.write_model(data, 'pointcloud_100.json')
        utils.validate_model(data)

        # data should contain "data" field
        layers = data.get('layers', {})
        features = layers[0].get('features')
        feature = features[0]
        self.assertIsNotNone(feature)
        self.assertTrue('data' in feature)

        # Add osm layer and write model file (for testing js)
        geo_map.createLayer('osm');
        # geo_map.center = {'x': -76.5, 'y': 43.0};
        # geo_map.zoom = 7;
        data = geo_map._build_data()
        #print(data)
        utils.write_model(data, 'pointcloud_100.json')


if __name__ == '__main__':
    unittest.main()

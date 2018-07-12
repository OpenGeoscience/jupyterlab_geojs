import os
import unittest

from . import utils
from jupyterlab_geojs import GeoJSMap, gdalutils


class TestPointCloudFeatures(unittest.TestCase):

    def test_las_100points(self):
        '''Test creating pointcloud feature'''
        filename = os.path.join(utils.data_folder, '100-points.las')

        geo_map = GeoJSMap()
        feature_layer = geo_map.createLayer('feature')
        pointcloud = feature_layer.createFeature('pointcloud', filename=filename)
        self.assertEqual(pointcloud.get_point_count(), 100)
        self.assertEqual(pointcloud.get_point_data_record_format(), 3)
        self.assertEqual(pointcloud.get_point_count_by_return(), (89, 10, 1, 0, 0))
        self.assertIsNone(pointcloud.get_wkt_string())

        bounds = pointcloud.get_bounds()
        min_x = 635717.85
        max_z = 530.61
        self.assertAlmostEqual(bounds[0], min_x)
        self.assertAlmostEqual(bounds[5], max_z)

        # atts = pointcloud.get_point_attributes()
        # print(atts)

        data = geo_map._build_data()

        utils.write_model(data, 'pointcloud-100_model.json')
        utils.validate_model(data)

        # data should contain "data" field
        layers = data.get('layers', {})
        features = layers[0].get('features')
        feature = features[0]
        self.assertIsNotNone(feature)
        self.assertTrue('data' in feature)

    def test_las_v14(self):
        '''Test that creating LAS version 1.4 not supported'''
        # Load as data instead of filename
        filename = os.path.join(utils.data_folder, 'test1_4.las')
        with open(filename, 'rb') as f:
            data = f.read()
        self.assertGreater(len(data), 30000)  # (sanity check)

        geo_map = GeoJSMap()
        feature_layer = geo_map.createLayer('feature')

        #pointcloud = feature_layer.createFeature('pointcloud', data=data)
        self.assertRaises(Exception, feature_layer.createFeature, 'pointcloud', data=data)

        # self.assertEqual(pointcloud.get_point_count(), 1000)
        # self.assertEqual(pointcloud.get_point_count_by_return(), (974, 23, 2, 1, 0))

        # bounds = pointcloud.get_bounds()
        # min_x = 1694038.4456376971
        # max_z = 5599.069686454539
        # self.assertAlmostEqual(bounds[0], min_x)
        # self.assertAlmostEqual(bounds[5], max_z)

        # self.assertIsNotNone(pointcloud.get_wkt_string())
        # # print(pointcloud.get_point_data_record_format())
        # # atts = pointcloud.get_point_attributes()
        # # print(atts)

        # if gdalutils.is_gdal_loaded():
        #     lonlat_bounds = pointcloud.get_bounds(as_lonlat=True)
        #     #print('lonlat_bounds: {}'.format(lonlat_bounds))
        #     min_x = -106.068729935  # (lon)
        #     max_y =   35.992260517  # (lat)
        #     self.assertAlmostEqual(lonlat_bounds[0], min_x, 6)  # lon min
        #     self.assertAlmostEqual(lonlat_bounds[3], max_y, 6)  # lat max

        # data = geo_map._build_data()

        # #utils.write_model(data, 'test1_4.json')
        # utils.validate_model(data)

        # # data should contain "data" field
        # layers = data.get('layers', {})
        # features = layers[0].get('features')
        # feature = features[0]
        # self.assertIsNotNone(feature)
        # self.assertTrue('data' in feature)

        # data = geo_map._build_data()
        #print(data)
        #utils.write_model(data, 'test1_4.json')


if __name__ == '__main__':
    unittest.main()

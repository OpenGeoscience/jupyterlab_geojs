"""
DEPRECATED
 * Was used for developing standalone pointcloud display
 * Replaced with pointcloud feature in Scene objects
"""


import os
import unittest

from . import utils
from jupyterlab_geojs import laspointcloud

@unittest.skip('Deprecated LASPointCloud')
class TestLASPointCloud(unittest.TestCase):
    '''Use unit test to generate test data for LASPointCloud

    '''

    def test_las_100points(self):
        '''Test creating pointcloud feature'''
        filename = os.path.join(utils.data_folder, '100-points.las')

        las = laspointcloud.LASPointCloud(filename)
        self.assertEqual(las._feature.get_point_count(), 100)
        self.assertIsNone(las._feature.get_wkt_string())

        data = las._feature._build_data()

        utils.write_model(data, 'laspointcloud_100.json')

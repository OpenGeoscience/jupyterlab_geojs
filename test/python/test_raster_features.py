import json
import os
import unittest

import jsonschema

from jupyterlab_geojs import GeoJSMap


source_dir = os.path.abspath(os.path.dirname(__file__))
data_dir = os.path.join(source_dir, os.pardir, 'data')


class TestRasterFeatures(unittest.TestCase):

    def test_rgb_image(self):
        '''Test creating raster feature'''
        filename = os.path.join(data_dir, 'rasterwithpalette.tif')

        geo_map = GeoJSMap()
        geo_map.center = {'x': -76.5, 'y': 43.0};
        geo_map.zoom = 7;
        geo_map.createLayer('osm');
        feature_layer = geo_map.createLayer('feature')
        feature_layer.createFeature('raster', filename=filename)

        data = geo_map._build_data()
        #print(data)

        schema_filename = os.path.join(source_dir, os.pardir, os.pardir, 'model', 'model.schema.json')
        schema = None
        with open(schema_filename) as f:
            schema_string = f.read()
        schema = json.loads(schema_string)
        print('validating against schema:')
        jsonschema.validate(data, schema)

        # Optionally write result to model file
        model_filename = os.path.join(source_dir, os.pardir, 'models', 'raster_model.json')
        data_string = json.dumps(data)
        with open(model_filename, 'w') as f:
            f.write(data_string)
            print('Wrote {}'.format(model_filename))

if __name__ == '__main__':
    unittest.main()

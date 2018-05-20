import json
import logging
import os
import sys
import unittest

import jsonschema

logging.basicConfig(level=logging.DEBUG)

from jupyterlab_geojs import GeoJSMap

ny_polygons = { "type": "Feature",
  "geometry": {
    "type": "Polygon",
    "coordinates": [[
      [-78.878369, 42.886447],
      [-76.147424, 43.048122],
      [-75.910756, 43.974784],
      [-73.756232, 42.652579],
      [-75.917974, 42.098687],
      [-78.429927, 42.083639],
      [-78.878369, 42.886447]
    ]]
  },
  "properties": {
    "author": "Kitware",
    "cities": ["Buffalo", "Syracuse", "Watertown", "Albany", "Binghamton", "Olean"]
  }
}

class TestGeoJSONFeatures(unittest.TestCase):

    def test_geojson_features(self):
        '''Test creating geojson features'''
        geo_map = GeoJSMap()
        geo_map.center = {'x': -76.5, 'y': 43.0};
        geo_map.zoom = 7;
        geo_map.createLayer('osm', renderer='canvas');
        feature_layer = geo_map.createLayer('feature')
        feature_layer.createFeature('geojson', data=ny_polygons)

        data = geo_map._build_data()
        #print(data)

        source_dir = os.path.abspath(os.path.dirname(__file__))
        schema_filename = os.path.join(source_dir, os.pardir, os.pardir, 'model', 'model.schema.json')
        schema = None
        with open(schema_filename) as f:
            schema_string = f.read()
        schema = json.loads(schema_string)
        print('validating against schema:')
        jsonschema.validate(data, schema)

        # Optionally write result to model file
        model_filename = os.path.join(source_dir, os.pardir, 'models', 'geojson_model.json')
        data_string = json.dumps(data)
        with open(model_filename, 'w') as f:
            f.write(data_string)
            print('Wrote {}'.format(model_filename))

if __name__ == '__main__':
    unittest.main()

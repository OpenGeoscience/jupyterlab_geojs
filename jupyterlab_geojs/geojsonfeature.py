import json
import os
from urllib.parse import urlparse

from . import gdalutils
from .geojsfeature import GeoJSFeature

class GeoJSONFeature(GeoJSFeature):
    ''''''
    def __init__(self, data, **kwargs):
        super(GeoJSONFeature, self).__init__('geojson', config_options=False, **kwargs)
        self._json_data = None
        self._uri = None

        # Determine if input data is filename, uri, or raw data
        filename = None
        if isinstance(data, str):
            parsed_url = urlparse(data)
            if not bool(parsed_url.scheme):
                # If not scheme, then we presume it is a file/path
                filename = data
            elif parsed_url.scheme == 'file':
                # If scheme is a file, strip the scheme and use the rest as file/path
                n = len('file://')
                filename = data[n:]
            else:
                # Otherwise infer it is a network url
                self._url = data
        elif isinstance(data, dict):
            self._json_data = data
        else:
            raise Exception('Unrecognized input data not a string or dict: {}'.format(data))

        if filename is not None:
            # Load data here, because javascript cannot load from
            # filesystem due to browser security restriction.
            if not os.path.exists(filename):
                raise Exception('Cannot find file {}'.format(filename))

            root, ext = os.path.splitext(filename)
            if ext == '.shp':
                # Convert shape files to geojson format
                self._json_data = self._convert_shp(filename)
            else:
                # Logic for standard geojson files
                with open(filename) as f:
                    text = f.read()
                self._json_data = json.loads(text)


    def _convert_shp(self, filename):
        '''Convert shp files to geojson data

        Returns feature collection object
        '''
        if not gdalutils.is_gdal_loaded():
            raise Exception('Cannot process .shp files because GDAL is not loaded')

        from osgeo import gdal, ogr
        # Create GeoJSON feature collection
        fc = {
            'type': 'FeatureCollection',
            'features': []
        }
        dataset = ogr.Open(filename, gdal.GA_ReadOnly)
        layer = dataset.GetLayer()
        for feature in layer:
            fc['features'].append(feature.ExportToJson(as_object=True))
        return fc

    def _build_display_model(self):
        display_model = super(GeoJSONFeature, self)._build_display_model()
        if self._json_data is not None:
            display_model['data'] = self._json_data
        elif self._url is not None:
            display_model['url'] = self._url
        return display_model

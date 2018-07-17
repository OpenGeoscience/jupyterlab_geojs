import json
import os

from . import gdalutils
from .geojsfeature import GeoJSFeature

class GeoJSONFeature(GeoJSFeature):
    ''''''
    def __init__(self, data=None, filename=None, url=None, **kwargs):
        super(GeoJSONFeature, self).__init__('geojson', config_options=False, **kwargs)
        self._data = None
        self._url = None

        if data is not None:
            self._data = data
        elif filename is not None:
            # Load data here, because javascript cannot load from
            # local filesystem due to browser security restriction.
            if not os.path.exists(filename):
                raise Exception('Cannot find file {}'.format(filename))

            root, ext = os.path.splitext(filename)
            if ext == '.shp':
                self._data = self._convert_shp(filename)
            else:
                # Logic for standard geojson files
                with open(filename) as f:
                    text = f.read()
                self._data = json.loads(text)
        if url is not None:
            self._url = url

        if self._data is None and self._url is None:
            raise Exception('Missing data, filename, or url argument')


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

    def _build_data(self):
        data = super(GeoJSONFeature, self)._build_data()
        if self._data is not None:
            data['data'] = self._data
        elif self._url is not None:
            data['url'] = self._url
        return data

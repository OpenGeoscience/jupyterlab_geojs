import json
import os

from .geojsfeature import GeoJSFeature

class GeoJSONFeature(GeoJSFeature):
    ''''''
    def __init__(self, data=None, filename=None, url=None, **kwargs):
        super(GeoJSONFeature, self).__init__('geojson', **kwargs)
        self._data = None
        self._url = None

        if data is not None:
            self._data = data
        elif filename is not None:
            # Load data here, because javascript cannot load from
            # local filesystem due to browser security restriction.
            if not os.path.exists(filename):
                raise Exception('Cannot find file {}'.format(filename))
            with open(filename) as f:
                text = f.read()
            self._data = json.loads(text)
        if url is not None:
            self._url = url

        if self._data is None and self._url is None:
            raise Exception('Missing data, filename, or url argument')

    def _build_data(self):
        data = super(GeoJSONFeature, self)._build_data()
        if self._data is not None:
            data['data'] = self._data
        elif self._url is not None:
            data['url'] = self._url
        return data

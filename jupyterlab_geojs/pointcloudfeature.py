import base64
import json
import os

from .geojsfeature import GeoJSFeature

class PointCloudFeature(GeoJSFeature):
    ''''''
    def __init__(self, data=None, filename=None, url=None, **kwargs):
        if data is None and filename is None and url is None:
            raise Exception('Missing data, filename, or url argument')

        super(PointCloudFeature, self).__init__('pointcloud', config_options=False, **kwargs)

        self._filename = None
        self._source_data = None
        self._url = None

        if data is not None:
            self._source_data = data
        elif filename is not None:
            self._filename = filename
            # Check that file exists
            if not os.path.exists(filename):
                raise Exception('Cannot find file {}'.format(filename))
        if url is not None:
            self._url = url


    def _build_data(self):
        '''Builds data model

        Represents point cloud data as either
          * uuencoded string
          * download url
        '''
        # Initialize output object
        data = super(PointCloudFeature, self)._build_data()

        # If source is a URL, have GeoJS download it
        if self._url:
            data['url'] = self._url
            return data

        # (else) Load point cloud here and send to client
        if self._source_data is None:
            with open(self._filename, 'rb') as f:
                self._source_data = f.read()

        # Encode the data
        encoded_bytes = base64.b64encode(self._source_data)
        # Have to decode as ascii so that Jupyter can jsonify
        encoded_string = encoded_bytes.decode('ascii')
        data['data'] = encoded_string
        return data

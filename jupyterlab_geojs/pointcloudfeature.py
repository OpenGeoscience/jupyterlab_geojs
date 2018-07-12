import base64
import os

from . import gdalutils
from .geojsfeature import GeoJSFeature
from .lasutils import LASMetadata, LASParser, LASPointAttributes

class PointCloudFeature(GeoJSFeature):
    ''''''
    def __init__(self, data=None, filenames=None, url=None, **kwargs):
        if data is None and filenames is None and url is None:
            raise Exception('Missing data, filenames, or url argument')

        super(PointCloudFeature, self).__init__('pointcloud', config_options=False, **kwargs)

        # Input source
        self._filenames = None
        self._source_data = None
        self._url = None

        # Other member data
        self._las_metadata = LASMetadata()

        if data is not None:
            self._source_data = data
        elif filenames is not None:
            self._filenames = filenames
            # Check that files exist
            for filename in filenames:
                if not os.path.exists(filename):
                    raise Exception('Cannot find file {}'.format(filename))
        if url is not None:
            self._url = url

        # parser = LASParser()
        # if self._source_data:
        #     import io
        #     instream = io.BytesIO(self._source_data)
        # elif self._filenames:
        #     instream = open(self._filename, 'rb')
        # elif self._url:
        #     raise Exception('Sorry - url input not yet supported')

        # try:
        #     self._las_metadata = parser.parse(instream)
        # except Exception:
        #     raise
        # finally:
        #     instream.close()

        # self._check_support()

        # print(self._las_metadata.header)
        # print(self._las_metadata.projection_wkt)

    def get_bounds(self, as_lonlat=False):
        '''Returns tuple (xmin,xmax,ymin,ymax,zmin,zmax)

        Converts xy components to lon/lat if flag is set (requires gdal)
        Returns None if required metadata not available
        '''
        h = self._las_metadata.header

        if as_lonlat:
            wkt = self.get_wkt_string()
            if wkt is None:
                raise Exception('Cannot convert points because WKT string is None')

            # Convert xy min & max points to lon lat
            native_points = [[h.min_x, h.min_y], [h.max_x, h.max_y]]
            lonlat = gdalutils.convert_points_to_lonlat(native_points, wkt)
            bounds = (lonlat[0][0],lonlat[1][0], lonlat[0][1],lonlat[1][1], h.min_z,h.max_z)
        else:
            bounds = (h.min_x,h.max_x, h.min_y,h.max_y, h.min_z,h.max_z)

        return bounds

    def get_las_header(self):
        '''Returns unpacked struct from LAS public header

        Returns None if source data is not LAS or LAZ
        '''
        return self._las_metadata.header

    def get_point_data_record_format(self):
        ''''''
        return self._las_metadata.header.point_data_record_format

    def get_point_attributes(self):
        '''Returns tuple of strings

        For LAS data, return value is based on point data record format
        '''
        format = self._las_metadata.header.point_data_record_format
        # Mod by 128, because LAZ headers add 128
        # Per http://www.cs.unc.edu/~isenburg/lastools/download/laszip.pdf
        format %= 128
        atts = LASPointAttributes.get(format)
        return atts

    def get_point_count(self):
        '''Returns unsigned long
        '''
        h = self._las_metadata.header
        if h.legacy_point_count:
            return h.legacy_point_count
        elif h.number_of_point_records:
            return h.number_of_point_records
        # (else)
        return None

    def get_point_count_by_return(self):
        ''' Returns standard LAS 5-tuple

        '''
        h = self._las_metadata.header
        if h.legacy_point_count:
            return h.legacy_number_of_points_by_return
        elif h.number_of_point_records:
            return h.number_of_points_by_return
        # (else)
        return None

    def get_proj_string(self):
        '''Returns Proj4 string

        Requires gdal to be installed in the python environment
        '''
        return None

    def get_wkt_string(self):
        '''Returns coordinate system WKT

        '''
        return self._las_metadata.projection_wkt


    def _build_data(self):
        '''Builds data model

        Represents point cloud data as either
          * uuencoded string
          * download url
        '''
        # Initialize output object
        data = super(PointCloudFeature, self)._build_data()

        # # If source is a URL, have GeoJS download it
        # if self._url:
        #     data['url'] = self._url
        #     return data

        # # (else) Load point cloud here and send to client
        # if self._source_data is None:
        #     with open(self._filename, 'rb') as f:
        #         self._source_data = f.read()

        # # Encode the data
        # encoded_bytes = base64.b64encode(self._source_data)
        # # Have to decode as ascii so that Jupyter can jsonify
        # encoded_string = encoded_bytes.decode('ascii')
        # data['data'] = encoded_string

        # Build an array of base64-encoded strings, one for each LAS file
        las_list = list()
        for filename in self._filenames:
            with open(filename, 'rb') as f:
                las_data = f.read()

            encoded_bytes = base64.b64encode(las_data)
            # Have to decode as ascii so that Jupyter can jsonify
            encoded_string = encoded_bytes.decode('ascii')
            las_list.append(encoded_string)

        data['data'] = las_list
        #print('las_list type {}: {}'.format(type(las_list), las_list))
        return data

    def _check_support(self):
        '''Checks las version and point record format.

        Our current code does not support all versions of las files:
        * Only supports file versions 1.0-1.3 (not 1.4)
        * Only supports point-record formats 0-3 (not 4-10)
        * Only supports uncompressed data (not laz)

        '''
        std_msg = 'Only LAS versions 1.0-1.3, point formats 0-3, no compression'
        h = self._las_metadata.header

        # Only LAS file versions 1.0 - 1.3
        version_string = '{}.{}'.format(h.version_major, h.version_minor)
        if h.version_major != 1 or h.version_minor > 3:
            raise Exception('INVALID: Cannot load LAS file version {}. {}'.format(
                version_string, std_msg))

        # Only uncompressed data
        if h.point_data_record_format >= 128:
            raise Exception('INVALID: Cannot load laz/compressed data. {}'.format(std_msg))

        # Only point record formats 0-3
        if h.point_data_record_format > 3:
            raise Exception('INVALID: Cannot load point record format {}. {}'.format(
                h.point_data_record_format, std_msg))

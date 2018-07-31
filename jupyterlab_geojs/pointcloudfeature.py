import base64
from operator import add
import os

from . import gdalutils
from .geojsfeature import GeoJSFeature
from .lasutils import LASMetadata, LASParser, LASPointAttributes

class PointCloudFeature(GeoJSFeature):
    ''''''
    def __init__(self, data, **kwargs):
        super(PointCloudFeature, self).__init__('pointcloud', config_options=False, **kwargs)

        # Input source
        self._bounds = None          # [xmin,xmax, ymin,ymax, zmin,zmax]
        self._filenames = None
        self._point_formats = dict() # <format, pointcount>
        self._point_count = 0
        self._point_count_by_return = [0]*5
        self._projection_wkt = ''

        # Note: this version of the feature only supports filename inputs,
        # not raw data or network url's
        if isinstance(data, list):
            self._filenames = data
        elif isinstance(data, str):
            self._filenames = [data]
        else:
            raise Exception('Input data is not list or string: {}'.format(data))
        # Check that files exist
        for f in self._filenames:
            if not os.path.exists(f):
                raise Exception('Cannot find file {}'.format(f))

        # Parse headers to initialize member data
        parser = LASParser()
        for i,filename in enumerate(self._filenames):
            metadata = None
            with open(filename, 'rb') as instream:
                metadata = parser.parse(instream)
                self._check_support(metadata)

            h = metadata.header
            if h.legacy_point_count:
                point_count = h.legacy_point_count
            else:
                point_count = h.number_of_point_records

            # Update bounds
            bounds = [h.min_x,h.max_x, h.min_y,h.max_y, h.min_z,h.max_z]
            if self._bounds is None:
                self._bounds = bounds
            else:
                for i in [0, 2, 4]:
                    if bounds[i] < self._bounds[i]:
                        self._bounds[i] = bounds[i]
                for i in [1, 3, 5]:
                    if bounds[i] > self._bounds[i]:
                        self._bounds[i] = bounds[i]

            # Update point formats
            format = h.point_data_record_format
            format_count = self._point_formats.get(format, 0)
            self._point_formats[format] = format_count + point_count

            # Update point count
            self._point_count += point_count

            # Update point count by return
            if h.legacy_number_of_points_by_return:
                self._point_count_by_return = list(map(add,
                    self._point_count_by_return,
                    h.legacy_number_of_points_by_return))
            else:
                self._point_count_by_return = list(map(add,
                    self._point_count_by_return,
                    h.number_of_points_by_return))

            # Update/check projection wkt
            if i == 0:
                self._projection_wkt = metadata.projection_wkt
            elif metadata.projection_wkt != self._projection_wkt:
                msg = ' '.join([
                    'Project mismatch between input files.'
                    'File {} is projection {}'.format(self._filenames[0], self._projection_wkt),
                    'File {} is projection {}'.format(self._filenames[i], metadata.projection_wkt)
                    ])
                raise Exception(msg)

    def get_bounds(self, as_lonlat=False):
        '''Returns tuple (xmin,xmax,ymin,ymax,zmin,zmax)

        '''
        return tuple(self._bounds)

    def get_point_data_record_formats(self):
        '''Returns dictionary of <format, point_count>

        '''
        return self._point_formats

    def get_point_attributes(self):
        '''Returns tuple of strings

        For LAS data, return value is based on point data record format
        '''
        format = self._point_data_record_format
        # Mod by 128, because LAZ headers add 128
        # Per http://www.cs.unc.edu/~isenburg/lastools/download/laszip.pdf
        format %= 128
        atts = LASPointAttributes.get(format)
        return atts

    def get_point_count(self):
        '''Returns unsigned long
        '''
        return self._point_count

    def get_point_count_by_return(self):
        ''' Returns standard LAS 5-tuple

        '''
        return tuple(self._point_count_by_return)

    def get_proj_string(self):
        '''Returns Proj4 string

        Requires gdal to be installed in the python environment
        '''
        if self._projection_wkt is None:
            return None
        elif gdalutils.is_gdal_loaded():
            from osgeo import osr
            proj = osr.SpatialReference()
            proj.ImportFromWkt(this._projection_wkt)
            return proj.ExportToProj4()
        else:
            raise Exception('Cannot convert projection because GDAL not installed')

        return None

    def get_wkt_string(self):
        '''Returns coordinate system WKT

        '''
        return self._projection_wkt


    def _build_display_model(self):
        '''Builds data model

        Represents point cloud data as list of uuencoded strings
        '''
        # Initialize output object
        display_model = super(PointCloudFeature, self)._build_display_model()

        # Build an array of base64-encoded strings, one for each LAS file
        las_list = list()
        for filename in self._filenames:
            with open(filename, 'rb') as f:
                las_data = f.read()

            encoded_bytes = base64.b64encode(las_data)
            # Have to decode as ascii so that Jupyter can jsonify
            encoded_string = encoded_bytes.decode('ascii')
            las_list.append(encoded_string)

        display_model['data'] = las_list
        #print('las_list type {}: {}'.format(type(las_list), las_list))
        return display_model

    def _check_support(self, metadata):
        '''Checks las version and point record format.

        Our current code does not support all versions of las files:
        * Only supports file versions 1.0-1.3 (not 1.4)
        * Only supports point-record formats 0-3 (not 4-10)
        * Only supports uncompressed data (not laz)

        '''
        if metadata is None:
            raise Exception('LAS Metadata missing')

        std_msg = 'Only LAS versions 1.0-1.3, point formats 0-3, no compression'
        h = metadata.header

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

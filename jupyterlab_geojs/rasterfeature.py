import base64
import json
import os
import pkg_resources
import time

from .geojsfeature import GeoJSFeature

'''
Raster features require GDAL to be installed on the kernel.
Check if GDAL is available
'''
try:
    pkg_resources.get_distribution('gdal')
except pkg_resources.DistributionNotFound:
    HAS_GDAL = False
else:
    HAS_GDAL = True
    from osgeo import gdal, osr

# Specify temp dir to use for copying gdal datasets
try:
    pkg_resources.get_distribution('jupyter_core.paths')
except pkg_resources.DistributionNotFound:
    pass
    TEMP_DIR = os.path.expanduser('~/.jupyterlab_geojs')
else:
    import jupyter_core.paths
    runtime_dir = jupyter_core.paths.jupyter_runtime_dir()
    TEMP_DIR = os.path.join(runtime_dir, 'geojs')
print('Using temp_dir {}'.format(TEMP_DIR))


class RasterFeature(GeoJSFeature):
    '''Initialize raster feature

    @param data GDALDataset
    @param filename string
    '''
    def __init__(self, data=None, filename=None, **kwargs):
        ''''''
        if not HAS_GDAL:
            raise Exception('Cannot create raster features -- GDAL not installed')

        if data is None and filename is None:
            raise Exception('Missing data or filename parameter -- one must be provided')

        # Model raster dataset as geojs quad feature with png image
        super(RasterFeature, self).__init__('quad', **kwargs)
        self._gdal_dataset = None

        if data is not None:
            if not isinstance(self._gdal_dataset, gdal.Dataset):
                raise Exception('Error - input data is not gdal.Dataset')
            self._data = data
        elif filename is not None:
            # Load data here, because javascript cannot load from
            # local filesystem due to browser security restriction.
            if not os.path.exists(filename):
                raise Exception('Cannot find file {}'.format(filename))

            # Load input file
            self._gdal_dataset = gdal.Open(filename, gdal.GA_ReadOnly)
            assert(self._gdal_dataset)

    def _build_data(self):
        '''Builds model as quad with image data'''
        data = super(RasterFeature, self)._build_data()
        options = data.get('options', {})

        # Set up coordinate transform to lonlat coordinates
        input_ref = osr.SpatialReference()
        input_ref.ImportFromWkt(self._gdal_dataset.GetProjection())
        lonlat_ref = osr.SpatialReference()
        lonlat_ref .ImportFromEPSG(4326)
        ref_transform = osr.CoordinateTransformation(input_ref, lonlat_ref)

        # Compute corner points
        gt = self._gdal_dataset.GetGeoTransform()
        if gt is None:
            raise Exception('Cannot render raster feature -- input has no geo transform')
        num_cols = self._gdal_dataset.RasterXSize
        num_rows = self._gdal_dataset.RasterYSize
        corners = list()
        for px in [0, num_cols]:
            for py in [0, num_rows]:
                native_x = gt[0] + px*gt[1] + py*gt[2]
                native_y = gt[3] + px*gt[4] + py*gt[5]

                # Convert to lon-lat
                x,y,z = ref_transform.TransformPoint(native_x, native_y)
                corners.append([x, y])

        # Feature data is array with image & corners points for each feature
        # We have only 1 feature
        # Set corner points
        feature_data = dict()
        feature_data['ul'] = {'x': corners[0][0], 'y': corners[0][1]}
        feature_data['ll'] = {'x': corners[1][0], 'y': corners[1][1]}
        feature_data['ur'] = {'x': corners[2][0], 'y': corners[2][1]}
        feature_data['lr'] = {'x': corners[3][0], 'y': corners[3][1]}
        #options['data'] = [data]

        # Get dataset's gcs
        projection = self._gdal_dataset.GetProjection()
        spatial_ref = osr.SpatialReference(wkt=projection)
        gcs_name = spatial_ref.GetAttrValue('AUTHORITY', 0)
        gcs_value = spatial_ref.GetAttrValue('AUTHORITY', 1)
        gcs_string = '{}:{}'.format(gcs_name, gcs_value)
        #print(gcs_string)
        #options['gcs'] = gcs_string

        # Need temp directory to create png dataset
        os.makedirs(TEMP_DIR, exist_ok=True)

        # Generate filename for interim png file
        # Use timestamp (presumes creating < 1 png image per second)
        ts = int(time.time())
        png_filename = '{}.png'.format(ts)

        # Create png dataset
        png_path = os.path.join(TEMP_DIR, png_filename)
        png_driver = gdal.GetDriverByName('PNG')
        png_dataset = png_driver.CreateCopy(png_path, self._gdal_dataset, strict=0)
        assert(png_dataset)
        png_dataset = None

        # Read png file and convert to base64 data
        with open(png_path, 'rb') as fp:
            encoded_bytes = base64.b64encode(fp.read())
        encoded_string = 'data:image/png;base64,' + encoded_bytes.decode('ascii')
        #print(encoded_string)
        feature_data['image'] = encoded_string

        options['data'] = [feature_data]
        data['options'] = options

        # Remove temp png file and return
        os.remove(png_path)
        return data

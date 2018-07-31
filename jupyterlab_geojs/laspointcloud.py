"""
DEPRECATED
 * Was used for developing standalone pointcloud display
 * Replaced with pointcloud feature in Scene objects
"""


import logging

from IPython.display import display, JSON

from .pointcloudfeature import PointCloudFeature

# An interim display class for point cloud data,
# essentially a wrapper for PointCloudFeature with new mime type
# Usage
#   from jupyterlab_geojs import LASPointCloud
#   LASPointCloud(LASFilename)

MIME_TYPE = 'application/las+json'


class LASPointCloud(JSON):
    def __init__(self, filename, **kwargs):
        """A display class for displaying pointcloud data in JupyterLab notebooks
        """
        super(LASPointCloud, self).__init__()
        self._feature = PointCloudFeature(filename=filename)
        self._logger = None


    def create_logger(self, folder, filename='laspointcloud.log'):
        '''Initialize logger with file handler

        @param folder (string) directory to store logfile
        '''
        os.makedirs(folder, exist_ok=True)  # create folder if needed

        log_name, ext = os.path.splitext(filename)
        self._logger = logging.getLogger(log_name)
        self._logger.setLevel(logging.INFO)  # default

        log_path = os.path.join(folder, filename)
        fh = logging.FileHandler(log_path, 'w')
        self._logger.addHandler(fh)
        return self._logger


    def _ipython_display_(self):
        ''''''
        if self._logger is not None:
            self._logger.debug('Enter LASPointCloud._ipython_display_()')

        display_model = self._feature._build_display_model()
        bundle = {
            MIME_TYPE: display_model,
            'text/plain': '<jupyterlab_geojs.LASPointCloud object>'
        }
        metadata = {
            MIME_TYPE: self.metadata
        }
        if self._logger is not None:
            self._logger.debug('display bundle: {}'.format(bundle))
            self._logger.debug('metadata: {}'.format(metadata))
        display(bundle, metadata=metadata, raw=True)

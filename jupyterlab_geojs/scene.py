import logging
import os

from IPython.display import display, JSON
from .geojsfeaturelayer import GeoJSFeatureLayer
from .geojsosmlayer import GeoJSOSMLayer
from .scenevalidator import SceneValidator
from .types import LayerType

# A display class that can be used in Jupyter notebooks:
#   from jupyterlab_geojs import Scene
#   Scene()

MIME_TYPE = 'application/geojs+json'


class Scene(JSON):
    """A display class for displaying GeoJS visualizations in the Jupyter Notebook and IPython kernel.

    Scene expects a JSON-able dict, not serialized JSON strings.

    Scalar types (None, number, string) are not allowed, only dict containers.
    """

    # List of options (names) to be added as a public member of each instance.
    # No error checking is done in this class.
    OptionNames = [
        'allowRotation',
        'center',
        'clampBoundsX',
        'clampBoundsY',
        'clampZoom',
        'discreteZoom',
        'gcs',
        'ingcs',
        'maxBounds',
        'minZoom',
        'maxZoom',
        'rotation',
        'unitsPerPixel',
        'zoom'
    ]

    def __init__(self, **kwargs):
        '''
        '''
        super(Scene, self).__init__()
        # Public members
        for name in self.__class__.OptionNames:
            value = kwargs.get(name)
            setattr(self, name, value)
        # Todo create attributes for any kwargs not in MemberNames,
        # for forward compatibility with GeoJS
        self._validator = SceneValidator()
        self._validator.adding_map(self)

        # Internal members
        self._options = kwargs
        self._layers = list()
        self._layer_lookup = dict()  # <layer, index>
        self._logger = None
        # Tracks the zoom & center coordinates in different representations
        self._viewpoint = type('ViewPoint', (object,), dict())
        self._viewpoint.mode = None
        self._viewpoint.bounds = {
            'left':   None,
            'top':    None,
            'right':  None,
            'bottom': None
        }

    def create_layer(self, layer_type, **kwargs):
        self._validator.adding_layer(self, layer_type)
        if False: pass
        # elif layer_type == 'annotation':
        #     layer = GeoJSAnnotationLayer(**kwargs)
        elif layer_type == LayerType.FEATURE:
            layer = GeoJSFeatureLayer(**kwargs)
        elif layer_type == LayerType.OSM:
            layer = GeoJSOSMLayer(**kwargs)
        # elif layer_type == 'ui':
        #     layer = GeoJSUILayer(**kwargs)
        else:
            raise Exception('Unrecognized layer type \"{}\"'.format(layerType))

        self._layers.append(layer)
        self._validator.added_layer(self, layer)
        return layer

    def create_logger(self, folder, filename='scene.log'):
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

    def set_zoom_and_center(self, enable=True, corners=None):
        '''Sets map zoom and center based on input args

        @param enable: (boolean) command geojs to set map's zoom & center coords
        @param corners: (list of [x,y]) bounding box specified by 4 corner points
        '''
        if not enable or corners is None:
            self._viewpoint.mode = None
        elif corners is not None:
            self._viewpoint.mode = 'bounds'
            x_coords,y_coords = zip(*corners)
            self._viewpoint.bounds['left']   = min(x_coords)
            self._viewpoint.bounds['right']  = max(x_coords)
            self._viewpoint.bounds['top']    = max(y_coords)
            self._viewpoint.bounds['bottom'] = min(y_coords)

    def _build_display_model(self):
        data = dict()  # return value

        # Copy options that have been set
        for name in self.__class__.OptionNames:
            value = getattr(self, name, None)
            if value is not None:
                self._options[name] = value
        data['options'] = self._options

        if self._viewpoint.mode is None:
            data['viewpoint'] = None
        else:
            data['viewpoint'] = {'mode': self._viewpoint.mode}
            if 'bounds' == self._viewpoint.mode:
                data['viewpoint']['bounds'] = self._viewpoint.bounds

        layer_list = list()
        for layer in self._layers:
            layer_list.append(layer._build_display_model())
        data['layers'] = layer_list
        return data


    def _ipython_display_(self):
        if self._logger is not None:
            self._logger.debug('Enter Scene._ipython_display_()')
        display_model = self._build_display_model()

        # Change mime type for "pointcloud mode"
        mimetype = 'application/las+json' if self._validator.is_pointcloud(self) else MIME_TYPE

        bundle = {
            mimetype: display_model,
            'text/plain': '<jupyterlab_geojs.Scene object>'
        }
        metadata = {
            mimetype: self.metadata
        }
        if self._logger is not None:
            self._logger.debug('display bundle: {}'.format(bundle))
            self._logger.debug('metadata: {}'.format(metadata))
        display(bundle, metadata=metadata, raw=True)

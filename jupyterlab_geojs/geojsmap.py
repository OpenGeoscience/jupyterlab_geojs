from IPython.display import display, JSON
from .geojsfeaturelayer import GeoJSFeatureLayer
from .geojsosmlayer import GeoJSOSMLayer

# A display class that can be used within a notebook.
#   from jupyterlab_geojs import GeoJSMap
#   GeoJSMap()

MIME_TYPE = 'application/geojs'

class GeoJSMap(JSON):
    """A display class for displaying GeoJS visualizations in the Jupyter Notebook and IPython kernel.

    GeoJSMap expects a JSON-able dict, not serialized JSON strings.

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
        super(GeoJSMap, self).__init__()
        # Public members
        for name in self.__class__.OptionNames:
            value = kwargs.get(name)
            setattr(self, name, value)
        # Todo create attributes for any kwargs not in MemberNames,
        # for forward compatibility with GeoJS

        # Internal members
        self._options = kwargs
        self._layers = list()
        self._layer_lookup = dict()  # <layer, index>

    def createLayer(self, layer_type, **kwargs):
        if False: pass
        # elif layer_type == 'annotation':
        #     layer = GeoJSAnnotationLayer(**kwargs)
        elif layer_type == 'feature':
            layer = GeoJSFeatureLayer(**kwargs)
        elif layer_type == 'osm':
            layer = GeoJSOSMLayer(**kwargs)
        # elif layer_type == 'ui':
        #     layer = GeoJSUILayer(**kwargs)
        else:
            raise Exception('Unrecognized layer type \"{}\"'.format(layerType))

        self._layers.append(layer)
        return layer

    def _build_data(self):
        data = dict()  # return value

        # Copy options that have been set
        for name in self.__class__.OptionNames:
            value = getattr(self, name, None)
            if value is not None:
                self._options[name] = value
        data['options'] = self._options

        layer_list = list()
        for layer in self._layers:
            layer_list.append(layer._build_data())
        data['layers'] = layer_list
        return data


    def _ipython_display_(self):
        data = self._build_data()
        bundle = {
            MIME_TYPE: data,
            'text/plain': '<jupyterlab_geojs.GeoJSMap object>'
        }
        metadata = {
            MIME_TYPE: self.metadata
        }
        display(bundle, metadata=metadata, raw=True)

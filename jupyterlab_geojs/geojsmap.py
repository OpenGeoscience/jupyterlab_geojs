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

    def __init__(self, center=None, zoom=None):
        '''
        '''
        super(GeoJSMap, self).__init__()
        # Public members
        self.center = center
        self.zoom = zoom

        # Internal members
        self._layers = list()
        self._layer_lookup = dict()  # <layer, index>

    def createLayer(self, layerType, **kwargs):
        if False: pass
        # elif layerType == 'annotation':
        #     layer = GeoJSAnnotationLayer(**kwargs)
        elif layerType == 'feature':
            layer = GeoJSFeatureLayer(**kwargs)
        elif layerType == 'osm':
            layer = GeoJSOSMLayer(**kwargs)
        # elif layerType == 'ui':
        #     layer = GeoJSUILayer(**kwargs)
        else:
            raise Exception('Unrecognized layer type \"{}\"'.format(layerType))

        self._layers.append(layer)
        return layer

    def _build_data(self):
        data = dict()  # return value

        options = dict()
        if self.center is not None: options['center'] = self.center
        if self.zoom is not None: options['zoom'] = self.zoom
        data['options'] = options

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

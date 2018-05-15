from IPython.display import display, JSON
from .geojsfeaturelayer import GeoJSFeatureLayer
from .geojsosmlayer import GeoJSOSMLayer

# A display class that can be used within a notebook. 
#   from jupyterlab_geojs import GeoJSMap
#   GeoJSMap(data)
    
class GeoJSMap(JSON):
    """A display class for displaying GeoJS visualizations in the Jupyter Notebook and IPython kernel.
    
    GeoJSMap expects a JSON-able dict, not serialized JSON strings.

    Scalar types (None, number, string) are not allowed, only dict containers.
    """

    def __init__(self, **kwargs):
        super(GeoJSMap, self).__init__()
        self._options = kwargs
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
        data = dict()
        data['options'] = self._options
        layer_list = list()
        for layer in self._layers:
            layer_list.append(layer._build_data())
        data['layers'] = layer_list
        return data


    def _ipython_display_(self):
        data = self._build_data()
        bundle = {
            'application/geojs': data,
            'text/plain': '<jupyterlab_geojs.GeoJSMap object>'
        }
        metadata = {
            'application/geojs': self.metadata
        }
        display(bundle, metadata=metadata, raw=True) 

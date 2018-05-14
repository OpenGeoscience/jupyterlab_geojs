from IPython.display import display, JSON
import json

# Running `npm run build` will create static resources in the static
# directory of this Python package (and create that directory if necessary).

def _jupyter_nbextension_paths():
    return [{
        'section': 'notebook',
        'src': 'nbextension',
        'dest': 'jupyterlab_geojs',
        'require': 'jupyterlab_geojs/extension'
    }]

# A display class that can be used within a notebook. 
#   from jupyterlab_geojs import GeoJSMap
#   GeoJSMap(data)
    
class GeoJSMap(JSON):
    """A display class for displaying GeoJS visualizations in the Jupyter Notebook and IPython kernel.
    
    GeoJS expects a JSON-able dict, not serialized JSON strings.

    Scalar types (None, number, string) are not allowed, only dict containers.
    """

    def _ipython_display_(self):
        bundle = {
            'application/geojs': self.data,
            'text/plain': '<jupyterlab_geojs.GeoJSMap object>'
        }
        metadata = {
            'application/geojs': self.metadata
        }
        display(bundle, metadata=metadata, raw=True) 

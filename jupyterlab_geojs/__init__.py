from .geojsmap import GeoJSMap

# Running `npm run build` will create static resources in the static
# directory of this Python package (and create that directory if necessary).

def _jupyter_nbextension_paths():
    return [{
        'section': 'notebook',
        'src': 'nbextension',
        'dest': 'jupyterlab_geojs',
        'require': 'jupyterlab_geojs/extension'
    }]

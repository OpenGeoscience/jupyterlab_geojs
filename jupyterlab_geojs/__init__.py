version_info = (0, 2, 0, 'dev')
__version__ = ".".join(map(str, version_info))

from .geojsmap import GeoJSMap


# def _jupyter_nbextension_paths():
#     return [{
#         'section': 'notebook',
#         'src': 'nbextension',
#         'dest': 'jupyterlab_geojs',
#         'require': 'jupyterlab_geojs/extension'
#     }]

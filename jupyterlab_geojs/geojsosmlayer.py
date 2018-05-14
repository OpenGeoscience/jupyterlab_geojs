

class GeoJSOSMLayer:
    """A notebook class for representing OSM layers in GeoJS visualizations.
    
    """

    def __init__(self, **kwargs):
        self._options = kwargs

    def _build_data(self):
        ''''''
        data = dict()
        data['layerType'] = 'osm'
        data['options'] = self._options
        return data

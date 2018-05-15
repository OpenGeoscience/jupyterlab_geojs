

class GeoJSFeatureLayer:
    """A notebook class for representing feature layers in GeoJS visualizations.

    """

    def __init__(self, **kwargs):
        self._options = kwargs

    def _build_data(self):
        ''''''
        data = dict()
        data['layerType'] = 'feature'
        data['options'] = self._options
        return data

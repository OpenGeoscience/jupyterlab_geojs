class GeoJSFeature:
    '''Abstract base class for all features
    '''
    def __init__(self, feature_type, **kwargs):
        self._feature_type = feature_type
        self._options = kwargs

    def _build_data(self):
        ''''''
        data = dict()
        data['featureType'] = self._feature_type
        data['options'] = self._options
        return data

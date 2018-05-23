from .geojsfeature import GeoJSFeature
from .geojslayer import GeoJSLayer
from .geojsonfeature import GeoJSONFeature

class GeoJSFeatureLayer:
    """A notebook class for representing feature layers in GeoJS visualizations.

    """
    OptionNames = GeoJSLayer.OptionNames + ['selectionAPI']

    def __init__(self, **kwargs):
        # Public members
        for name in self.__class__.OptionNames:
            value = kwargs.get(name)
            setattr(self, name, value)
        # Todo create attributes for any kwargs not in MemberNames,
        # for forward compatibility with GeoJS

        # Internal members
        self._options = kwargs
        self._features = list()

    def createFeature(self, feature_type, **kwargs):
        '''API method to add features to this layer'''
        if feature_type == 'geojson':  # special case
            feature = GeoJSONFeature(**kwargs)
        else:
            feature = GeoJSFeature(feature_type, **kwargs)

        self._features.append(feature)
        return feature


    def _build_data(self):
        ''''''
        data = dict()  # return value
        data['layerType'] = 'feature'

        # Copy options that have been set
        for name in self.__class__.OptionNames:
            value = getattr(self, name, None)
            if value is not None:
                self._options[name] = value
        data['options'] = self._options

        feature_data = list()
        for feature in self._features:
            feature_data.append(feature._build_data())
        data['features'] = feature_data

        return data

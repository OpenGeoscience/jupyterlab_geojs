from .geojsfeature import GeoJSFeature
from .geojslayer import GeoJSLayer
from .geojsonfeature import GeoJSONFeature
from .pointcloudfeature import PointCloudFeature
from .rasterfeature import RasterFeature
from .scenevalidator import SceneValidator
from .types import FeatureType


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
        self._validator = SceneValidator()

    def create_feature(self, feature_type, data, **kwargs):
        '''API method to add features to this layer'''
        self._validator.adding_feature(self, feature_type)

        # Handle special cases first
        if feature_type == FeatureType.GEOJSON:
            feature = GeoJSONFeature(data, **kwargs)
        elif feature_type == FeatureType.POINTCLOUD:
            feature = PointCloudFeature(data, **kwargs)
        elif feature_type == FeatureType.POLYGON and isinstance(data, str):
            # Special case: polygon with string data represents shp file
            # Load shp file as geojson feature
            feature = GeoJSONFeature(data, **kwargs)
        elif feature_type == FeatureType.RASTER:
            feature = RasterFeature(data, **kwargs)
        else:
            feature = GeoJSFeature(feature_type, data=data, **kwargs)

        self._features.append(feature)
        return feature

    def clear(self):
        '''Removes all features from this layer

        '''
        self._validator.clearing_layer(self)
        del self._features[:]


    def _build_display_model(self):
        ''''''
        display_model = dict()  # return value
        display_model['layerType'] = 'feature'

        # Copy options that have been set
        for name in self.__class__.OptionNames:
            value = getattr(self, name, None)
            if value is not None:
                self._options[name] = value
        display_model['options'] = self._options

        feature_data = list()
        for feature in self._features:
            feature_data.append(feature._build_display_model())
        display_model['features'] = feature_data

        return display_model

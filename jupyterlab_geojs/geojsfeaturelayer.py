from .geojslayer import GeoJSLayer

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

        return data

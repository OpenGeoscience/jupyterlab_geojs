from .geojslayer import GeoJSLayer

class GeoJSOSMLayer:
    """A notebook class for representing OSM layers in GeoJS visualizations.

    """
    OptionNames = GeoJSLayer.OptionNames

    def __init__(self, **kwargs):
        ''''''
        # Public members
        for name in self.__class__.OptionNames:
            value = kwargs.get(name)
            setattr(self, name, value)
        # Todo create attributes for any kwargs not in MemberNames,
        # for forward compatibility with GeoJS

        # Internal members
        self._options = kwargs

    def _build_display_model(self):
        ''''''
        display_model = dict()  # return value
        display_model['layerType'] = 'osm'

        # Copy options that have been set
        for name in self.__class__.OptionNames:
            value = getattr(self, name, None)
            if value is not None:
                self._options[name] = value
        display_model['options'] = self._options

        return display_model



class GeoJSLayer:
    '''Incomplete class listing common options for all layers.

    This is NOT a base class for concrete layer classes.
    The OptionNames list in this class should be included in all concrete layer classes
    '''
    OptionNames = [
        'active',
        'attribution',
        'name',
        'opacity',
        'rendererName',
        'visible',
        'zIndex'
    ]

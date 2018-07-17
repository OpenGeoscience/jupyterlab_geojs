class GeoJSFeature:
    '''Generic/base class for map features
    '''

    # List of options that are common to all GoeJS features
    CommonOptionNames = [
        'bin',
        'data',
        'gcs',
        'selectionAPI',
        'style',
        'visible'
    ]

    # Table of options specific to each feature type
    OptionNameTable = {
        'point': ['colormap', 'enableTooltip', 'position'],
        'quad': ['image', 'imageCrop', 'imageFixedScale']  # omit 'color' 'canvas', 'video'
    }

    def __init__(self, feature_type, config_options=True, **kwargs):
        # Public members
        option_names = []
        if config_options:
            option_names = self.__class__.CommonOptionNames + \
                self.__class__.OptionNameTable.get(feature_type, [])
            for name in option_names:
                value = kwargs.get(name)
                setattr(self, name, value)
            # Todo create attributes for any kwargs not in MemberNames,
            # for forward compatibility with GeoJS

        # Internal members
        self._feature_type = feature_type
        self._options = kwargs
        self._option_names = option_names

    def _build_data(self):
        ''''''
        data = dict()
        data['featureType'] = self._feature_type

        # Add selection workaround for points
        if self._feature_type == 'point' \
            and isinstance(self._options['data'], list) \
            and len(self._options['data']) > 0 \
            and not '__i' in self._options['data'][0]:

            for i in range(len(self._options['data'])):
                self._options['data'][i]['__i'] =i

        # Copy options that have been set
        for name in self._option_names:
            value = getattr(self, name, None)
            if value is not None:
                self._options[name] = value
        data['options'] = self._options

        return data

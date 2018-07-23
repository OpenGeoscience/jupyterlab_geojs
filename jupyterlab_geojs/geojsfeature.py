class GeoJSFeature:
    '''Generic/base class for GeoJS features
    '''

    # List of options that are common to all GoeJS features
    CommonOptionNames = [
        'bin',
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

    def _build_display_model(self):
        ''''''
        display_model = dict()
        display_model['featureType'] = self._feature_type

        # Add selection workaround for points
        if self._feature_type == 'point':
            point_data = self._options.get('data')
            if isinstance(point_data, list) \
                and len(point_data) > 0 \
                and not '__i' in point_data[0]:

                for i in range(len(point_data)):
                    point_data[i]['__i'] = i
            self._options['data'] = point_data

        # Copy options that have been set
        for name in self._option_names:
            value = getattr(self, name, None)
            if value is not None:
                self._options[name] = value

        # Apply any lambda functions
        data = self._options.get('data')

        # Check position
        position = self._options.get('position')
        if position is not None and callable(position):
            position_coords = [position(item) for item in data]
            self._options['position'] = position_coords

        # Check style components
        style = self._options.get('style', {})
        for key,val in style.items():
            if callable(val):
                item_vals = [val(item) for item in data]
                style[key] = item_vals

        display_model['options'] = self._options

        return display_model

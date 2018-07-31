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

        # Add array index to point features, because it:
        #   - provides a selection workaround for points
        #   - is used in client for options specified by function
        # Should this index be added to all feature types?
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

                # Check format for styles that set color
                if key in ['backgroundColor', 'color', 'fillColor', 'strokeColor']:
                    item_vals = self._format_colors(item_vals)
                style[key] = item_vals

        display_model['options'] = self._options

        return display_model

    def _format_colors(self, input_vals):
        '''Converts input colors to hex format.

        This only applies to colors produced by a callable
        '''
        # Use first item as exemplar
        input0 = input_vals[0]
        # Abort for unexpected input
        if not isinstance(input0, (list,tuple)):
            return input_vals
        if len(input0) < 3 or len(input0) > 4:
            return input_vals
        if len(input0) == 4:
            input0 = list(input0[:3])

        if max(input0) <= 1:
            return[self._double_to_hex(item) for item in input_vals]
        elif max(input0) <= 255:
            return [self._rgb_to_hex(item) for item in input_vals]

        # else:
        return input_vals  # dont understand format


    def _double_to_hex(self, color):
        rgb = tuple(map(lambda val: int(255.0 * val), color))
        return self._rgb_to_hex(rgb)

    def _rgb_to_hex(self, rgb):
        hexVal = tuple(map(lambda val: '{:02x}'.format(val), rgb[:3]))
        return '#' + ''.join(hexVal)

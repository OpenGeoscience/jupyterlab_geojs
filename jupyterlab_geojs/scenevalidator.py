"""Validates scenes before creating layers and features,

Currently, this extension can render maps containing either,
but not both:
 * Regular GeoJS layers and features
 * One feature layer with one point cloud feature

 To make things work via a single class (Scene), this class
 checks each new layer and feature as it is created, and raises an
 Exception if the current limitations are not met. The intent is to
 isolate as much of the validity-checking code as possible, with the
 expectation it will not be needed in the future, once geojs can
 support vtk.js layers.
"""

from enum import Enum

class _SceneMode(Enum):
    '''For specifying a model on map instance; used by scene validator

    '''
    UNASSIGNED = 'unassigned'  # scene contains no osm layer or no features
    GEOJS = 'geojs'            # scene contains osm layer or non-pointcloud features
    POINTCLOUD = 'pointcloud'  # scen contains pointcloud feature(s)


class _SceneValidator:
    instance = None

    def __init__(self):
        # Enforce singleton pattern
        if _SceneValidator.instance:
            raise Exception('Error creating _SceneValidator - use scene_validator instead')

        self._mapDict = dict()    # <Scene instance, _SceneMode>
        self._layerDict = dict()  # <GeoJSLayer instance, Scene instance>

    def adding_map(self, map):
        '''This must be called when a new Scene instance is initialized

        '''
        assert(not map in self._mapDict)
        self._mapDict[map] = _SceneMode.UNASSIGNED

    def adding_layer(self, map, layer_type):
        mode = self._mapDict[map]
        #print('Adding layer type {} to map mode {}'.format(layer_type, mode))
        if mode == _SceneMode.UNASSIGNED:
            if layer_type == 'osm':
                self._mapDict[map] = _SceneMode.GEOJS
        elif mode == _SceneMode.POINTCLOUD:
            raise Exception('Cannot add osm layer to scene containing a pointcloud object')


    def added_layer(self, map, layer):
        '''This must be called AFTER each layer is added to a map

        '''
        self._layerDict[layer] = map

    def adding_feature(self, layer, feature_type):
        '''This must be called BEFORE adding a feature

        '''
        map = self._layerDict[layer]
        mode = self._mapDict[map]
        #print('Adding feature type {} to map mode {}'.format(feature_type, mode))
        if mode == _SceneMode.UNASSIGNED:
            if feature_type == 'pointcloud':
                self._mapDict[map] = _SceneMode.POINTCLOUD
            else:
                self._mapDict[map] = _SceneMode.GEOJS
        elif mode == _SceneMode.GEOJS:
            if feature_type == 'pointcloud':
                raise Exception('Cannot add pointcloud to scene with osm layer or geojs features')
        elif mode == _SceneMode.POINTCLOUD:
            if feature_type == 'pointcloud':
                raise Exception('Cannot use multiple pointcloud features in one scene')
            else:
                raise Exception('Cannot add non-pointcloud feature to scene containing pointcloud features')

    def clearing_layer(self, layer):
        '''Checks if layer has pointcloud feature, and resets if applicable

        '''
        map = self._layerDict[layer]
        mode = self._mapDict[map]
        if mode != _SceneMode.POINTCLOUD:
            return

        # Rest mode if this layer contains a (pointcloud) feature
        if len(layer._features) == 1:
            self._mapDict[map] = _SceneMode.UNASSIGNED

    def is_pointcloud(self, map):
        '''Returns boolean indicating whether specific map is pointcloud type

        '''
        return self._mapDict.get(map) == _SceneMode.POINTCLOUD


def SceneValidator():
    if _SceneValidator.instance is None:
        _SceneValidator.instance = _SceneValidator()
    return _SceneValidator.instance

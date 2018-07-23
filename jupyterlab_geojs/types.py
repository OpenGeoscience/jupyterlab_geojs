# Enumerated classes which can be used to specify layer or feature types.
# These classes are for convenience only (you can always use a string).

class LayerType:
    '''For Scene.create_layer()'''
    OSM     = 'osm'
    FEATURE = 'feature'
    #UI = 'ui'  # (future)


class FeatureType:
    '''For GeoJSFeatureLayer.create_feature()'''
    GEOJSON    = 'geojson'
    POINT      = 'point'
    POINTCLOUD = 'pointcloud'
    POLYGON    = 'polygon'
    QUAD       = 'quad'
    RASTER     = 'raster'

'''
A set of GDAL related utils
'''
import pkg_resources

try:
    pkg_resources.get_distribution('gdal')
except pkg_resources.DistributionNotFound:
    HAS_GDAL = False
else:
    HAS_GDAL = True
    from osgeo import gdal, osr


def is_gdal_loaded():
    return HAS_GDAL


def convert_points_to_lonlat(points, projection_wkt):
    '''Converts an array of points to lonlat coordinates

    '''
    if not is_gdal_loaded():
        raise Exception('Cannot convert points because GDAL not loaded')

    from_spatial_ref = osr.SpatialReference()
    from_spatial_ref.ImportFromWkt(projection_wkt)

    lonlat_ref = osr.SpatialReference()
    lonlat_ref .ImportFromEPSG(4326)
    ref_transform = osr.CoordinateTransformation(from_spatial_ref, lonlat_ref)

    n = len(points)
    lonlat_points = [None] * n
    for i,point in enumerate(points):
        input_x = point[0]
        input_y = point[1]
        x,y,z = ref_transform.TransformPoint(input_x, input_y)
        lonlat_points[i] = [x, y]
    return lonlat_points

def convert_wkt_to_proj(projection_wkt):
    '''Converts projection WKT string to Proj4 string

    '''
    if not is_gdal_loaded():
        raise Exception('Cannot convert projection WKT because GDAL not loaded')

    if projection_wkt is None:
        return None

    ref = osr.SpatialReference()
    ref.ImportFromWkt(wkt)
    proj4_string = ref.ExportToProj4()
    return proj4_string

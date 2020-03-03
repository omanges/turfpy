from geojson import Point, Polygon, MultiPolygon, MultiPoint, LineString, MultiLineString, FeatureCollection, Feature
from math import radians, sin, cos, degrees, atan2, asin, sqrt
from typing import Union
from turfpy.meta import geom_reduce, coord_each


# ---------- Bearing -----------#

def bearing(start: Point, end: Point, final=False):
    """
    Takes two {@link Point} and finds the geographic bearing between them,
    :param Point start: Start point
    :param Point end: Ending point
    :param boolean final:
    :return float: calculates the final bearing if true

    Example :-
    >>> from turfpy import measurement
    >>> from geojson import Point
    >>> start = Point((-75.343, 39.984))
    >>> end = Point((-75.534, 39.123))
    >>> measurement.bearing(start,end)
    """
    if final:
        return calculate_final_bearing(start, end)
    start_coordinates = start['coordinates']
    end_coordinates = end['coordinates']
    lon1 = radians(float(start_coordinates[0]))
    lon2 = radians(float(end_coordinates[0]))
    lat1 = radians(float(start_coordinates[1]))
    lat2 = radians(float(end_coordinates[1]))

    a = sin(lon2 - lon1) * cos(lat2)

    b = (cos(lat1) * sin(lat2)) - (sin(lat1) * cos(lat2) * cos(lon2 - lon1))
    return degrees(atan2(a, b))


def calculate_final_bearing(start, end):
    bear = bearing(end, start)
    bear = (bear + 180) % 360
    return bear


# -------------------------------#

# ---------- Distance -----------#

def distance(point1: Point, point2: Point, unit: str = 'km'):
    """
    Calculates distance between two Points. A point is containing latitude and
    logitude in decimal degrees and ``unit`` is optional.
    It calculates distance in units such as kilometers, meters, miles, feet and inches.
    :param point1: first point; tuple of (latitude, longitude) in decimal degrees
    :param point2: second point; tuple of (latitude, longitude) in decimal degrees
    :param unit: A string containing unit, E.g. kilometers = 'km', miles = 'mi',
    meters = 'm', feet = 'ft', inches = 'in'.
    Example :-

    >>> from turfpy import measurement
    >>> from geojson import Point
    >>> start = Point((-75.343, 39.984))
    >>> end = Point((-75.534, 39.123))
    >>> measurement.distance(start,end)

    :return: The distance between the two points in the requested unit, as a float.
    """
    avg_earth_radius_km = 6371.0088
    conversions = {'km': 1.0, 'm': 1000.0, 'mi': 0.621371192,
                   'ft': 3280.839895013, 'in': 39370.078740158
                   }
    lat1, lon1 = point1['coordinates']
    lat2, lon2 = point2['coordinates']

    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    lat = lat2 - lat1
    lon = lon2 - lon1
    d = sin(lat * 0.5) ** 2 + cos(lat1) * cos(lat2) * sin(lon * 0.5) ** 2
    return 2 * avg_earth_radius_km * conversions[unit] * asin(sqrt(d))


# -------------------------------#

# ----------- Area --------------#

def area(geojson: Union[
    Point, LineString, Polygon, MultiPoint, MultiLineString, MultiPolygon, Feature, FeatureCollection]):
    """
    This function calculates the area of the Geojson object given as input.
    :param geojson: Geojson object for which area is to be found
    :return: area for the given Geojson object
    Example :-

    >>> from turfpy.measurement import area
    >>> from geojson import Feature, FeatureCollection

    >>> geometry_1 = {"coordinates": [[[0, 0], [0, 10], [10, 10], [10, 0], [0, 0]]], "type": "Polygon"};
    >>> geometry_2 = {"coordinates": [[[2.38, 57.322], [23.194, -20.28], [-120.43, 19.15], [2.38, 57.322]]], "type": "Polygon"};
    >>> feature_1 = Feature(geometry=geometry_1)
    >>> feature_2 = Feature(geometry=geometry_2)
    >>> feature_collection = FeatureCollection([feature_1, feature_2])

    >>> area(feature_collection)
    """
    return geom_reduce(geojson, 0)


# -------------------------------#

# ----------- BBox --------------#
result = [float('inf'), float('inf'), float('-inf'), float('-inf')]


def bbox(geojson):
    """
    This function is used to generate bounding box coordinates for given geojson
    :param geojson: Geojson object for which bounding box is to be found
    :return: bounding box for the given Geojson object
    Example :-

    >>> from turfpy.measurement import bbox
    >>> from geojson import Polygon

    >>> p = Polygon([[(2.38, 57.322), (23.194, -20.28), (-120.43, 19.15), (2.38, 57.322)]])
    >>> bb = bbox(p)
    """
    global result
    result = [float('inf'), float('inf'), float('-inf'), float('-inf')]
    coord_each(geojson, callback_coord_each)
    return result


def callback_coord_each(coord):
    global result
    if result[0] > coord[0]:
        result[0] = coord[0]
    if result[1] > coord[1]:
        result[1] = coord[1]
    if result[2] < coord[0]:
        result[2] = coord[0]
    if result[3] < coord[1]:
        result[3] = coord[1]


# -------------------------------#

# ----------- BBoxPolygon --------------#

def bbox_polygon(bbox: list, properties: dict = {}) -> Feature:
    """
    To generate a Polygon Feature for the bounding box generated using bbox.
    :param properties: properties to be added to the returned feature
    :param bbox: bounding box generated for a geojson.
    :return: polygon for the given bounding box coordinates
    Example :-
    >>> from turfpy.measurement import bbox
    >>> from geojson import Polygon

    >>> p = Polygon([[(2.38, 57.322), (23.194, -20.28), (-120.43, 19.15), (2.38, 57.322)]])
    >>> bb = bbox(p)
    >>> feature = bbox_polygon(bb)
    """
    west = float(bbox[0])
    south = float(bbox[1])
    east = float(bbox[2])
    north = float(bbox[3])

    if len(bbox) == 6:
        raise Exception("bbox-polygon does not support BBox with 6 positions")

    low_left = (west, south)
    top_left = (west, north)
    top_right = (east, north)
    low_right = (east, south)

    bbox_polygon = Polygon([[low_left, low_right, top_right, top_left, low_left]])
    feature_bbox = Feature(geometry=bbox_polygon)

    if 'properties' in properties:
        feature_bbox.properties = properties['properties']
    elif 'properties' not in properties:
        feature_bbox.properties = {}

    if 'id' in properties:
        feature_bbox.id = properties['id']

    if 'bbox' in properties:
        feature_bbox.bbox = properties['bbox']

    return feature_bbox


# -------------------------------#

# ----------- Center --------------#

def center(geojson, properties: dict = {}) -> Feature:
    """
    Takes a {@link Feature} or {@link FeatureCollection} and returns the absolute center point of all features.
    :param geojson: geojson GeoJSON to be centered
    :param properties: Optional parameters to be set to the generated feature
    :return: Point feature for the center
    Example :-
    >>> from turfpy.measurement import center
    >>> from geojson import Feature, FeatureCollection

    >>> f1 = Feature(geometry=Point((-97.522259, 35.4691)))
    >>> f2 = Feature(geometry=Point((-97.502754, 35.463455)))
    >>> f3 = Feature(geometry=Point((-97.508269, 35.463245)))
    >>> feature_collection = FeatureCollection([f1, f2, f3])
    >>> feature = center(feature_collection)
    """
    bounding_box = bbox(geojson)
    x = (bounding_box[0] + bounding_box[2]) / 2;
    y = (bounding_box[1] + bounding_box[3]) / 2;

    point = Point((x, y))

    center_feature = Feature(geometry=point)

    if 'properties' in properties:
        center_feature.properties = properties['properties']
    elif 'properties' not in properties:
        center_feature.properties = {}

    if 'id' in properties:
        center_feature.id = properties['id']

    if 'bbox' in properties:
        center_feature.bbox = properties['bbox']

    return center_feature


# -------------------------------#

# ----------- Envelope --------------#

def envelope(geojson) -> Feature:
    """
    Takes any number of features and returns a rectangular {@link Polygon} that encompasses all vertices.
    :param geojson: geojson input features for which envelope to be generated
    :return:
    Example :-
    >>> from turfpy.measurement import envelope
    >>> from geojson import Feature, FeatureCollection

    >>> f1 = Feature(geometry=Point((-97.522259, 35.4691)))
    >>> f2 = Feature(geometry=Point((-97.502754, 35.463455)))
    >>> f3 = Feature(geometry=Point((-97.508269, 35.463245)))
    >>> feature_collection = FeatureCollection([f1, f2, f3])
    >>> feature = envelope(feature_collection)
    """
    return bbox_polygon(bbox(geojson))
# -------------------------------#

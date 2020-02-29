from geojson import Point, Polygon, MultiPolygon, MultiPoint, LineString, MultiLineString, FeatureCollection, Feature
from math import radians, sin, cos, degrees, atan2, asin, sqrt, pi
from typing import  Union

RADIUS = 6378137;


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

def area(geojson: Union[Point, LineString, Polygon, MultiPoint, MultiLineString, MultiPolygon, Feature, FeatureCollection]):
    return geom_reduce(geojson, 0)


initial_value = ''
previous_value = ''


def geom_reduce(geojson, initial_value_param):
    global initial_value
    global previous_value
    initial_value = initial_value_param
    previous_value = initial_value_param
    geom_each(geojson, callback_geom_each)
    return previous_value


def geom_each(geojson, callback):
    feature_index = 0
    is_feature_collection = geojson['type'] == 'FeatureCollection'
    is_feature = geojson['type'] == 'Feature'
    stop = len(geojson['features']) if is_feature_collection else 1
    for i in range(0, stop):
        if is_feature_collection:
            geometry_maybe_collection = geojson['features'][i]['geometry']
            feature_properties = geojson['features'][i].get('properties')
            feature_b_box = geojson['features'][i].get('bbox')
            feature_id = geojson['features'][i].get('id')
        elif is_feature:
            geometry_maybe_collection = geojson['geometry']
            feature_properties = geojson.get('properties')
            feature_b_box = geojson.get('bbox')
            feature_id = geojson.get('id')
        else:
            geometry_maybe_collection = geojson
            feature_properties = {}
            feature_b_box = None
            feature_id = None

        if geometry_maybe_collection:
            if geometry_maybe_collection['type'] == 'GeometryCollection':
                is_geometry_collection = True
            else:
                is_geometry_collection = False
        stop_g = len(geometry_maybe_collection['geometries']) if is_geometry_collection else 1

        for g in range(0, stop_g):
            geometry = geometry_maybe_collection['geometries'][
                g] if is_geometry_collection else geometry_maybe_collection

            if not geometry:
                if not callback(None, feature_index, feature_properties, feature_b_box, feature_id):
                    return False
                continue

            if geometry['type'] == 'Point' \
                    or geometry['type'] == 'LineString' \
                    or geometry['type'] == 'MultiPoint' \
                    or geometry['type'] == 'Polygon' \
                    or geometry['type'] == 'MultiLineString' \
                    or geometry['type'] == 'MultiPolygon':
                if not callback(geometry, feature_index, feature_properties, feature_b_box, feature_id):
                    return False
                break
            elif geometry['type'] == 'GeometryCollection':
                for j in range(0, len(geometry['geometries'])):
                    if not callback(geometry['geometries'][j], feature_index, feature_properties, feature_b_box,
                                    feature_id):
                        return False
                break
            else:
                raise Exception('Unknown Geometry Type')
        feature_index += feature_index + 1


def callback_geom_each(current_geometry, feature_index, feature_properties, feature_bbox, feature_id):
    global initial_value
    global previous_value
    if feature_index == 0 and initial_value:
        previous_value = current_geometry
    else:
        previous_value = callback_geom_reduce(previous_value, current_geometry)
    return previous_value


def callback_geom_reduce(value, geom):
    return value + calculate_area(geom)


def calculate_area(geom) -> float:
    total = 0
    if geom['type'] == 'Polygon':
        return polygon_area(geom['coordinates'])
    elif geom['type'] == 'MultiPolygon':
        for coords in geom['coordinates']:
            total += polygon_area(coords)
            return total
    elif geom['type'] == 'Point' \
            or geom['type'] == 'MultiPoint' \
            or geom['type'] == 'LineString' \
            or geom['type'] == 'MultiLineString':
        return 0
    return 0


def polygon_area(coords: list):
    total = 0

    if coords and len(coords) > 0:
        total += abs(ring_area(coords[0]))
        for i in range(1, len(coords)):
            total -= abs(ring_area(coords[i]))

    return total


def ring_area(coords: list):
    total = 0
    coords_length = len(coords)

    if coords_length > 2:
        for i in range(0, coords_length):
            if i == coords_length - 2:
                lower_index = coords_length - 2
                middle_index = coords_length - 1
                upper_index = 0
            elif i == coords_length - 1:
                lower_index = coords_length - 1
                middle_index = 0
                upper_index = 1
            else:
                lower_index = i
                middle_index = i + 1
                upper_index = i + 2

            p1 = coords[lower_index]
            p2 = coords[middle_index]
            p3 = coords[upper_index]
            total += (rad(p3[0]) - rad(p1[0])) * sin(rad(p2[1]))

        total = total * RADIUS * RADIUS / 2
    return total


def rad(num: float):
    return num * pi / 180
# -------------------------------#

from geojson import Point, Polygon, MultiPolygon, MultiPoint, LineString, MultiLineString, FeatureCollection, Feature
from math import radians, sin, cos, degrees, atan2, asin, sqrt, pow, pi, log, tan
from typing import Union
from turfpy.meta import geom_reduce, coord_each, segment_reduce, feature_each, segment_each
from turfpy.helper import radians_to_length, length_to_radians, get_coords, get_coord, get_geom, get_type, \
    convert_length, feature_of, avg_earth_radius_km


# ---------- Bearing -----------#

def bearing(start: Point, end: Point, final=False):
    """
    Takes two Point and finds the geographic bearing between them.
    :param Point start: Start point.
    :param Point end: Ending point.
    :param boolean final: calculates the final bearing if true.
    :return float: calculated bearing.
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

def distance(point1: Point, point2: Point, units: str = 'km'):
    """
    Calculates distance between two Points. A point is containing latitude and
    logitude in decimal degrees and ``unit`` is optional.
    It calculates distance in units such as kilometers, meters, miles, feet and inches.
    :param point1: first point; tuple of (latitude, longitude) in decimal degrees.
    :param point2: second point; tuple of (latitude, longitude) in decimal degrees.
    :param units: A string containing unit, E.g. kilometers = 'km', miles = 'mi',
    meters = 'm', feet = 'ft', inches = 'in'.
    :return: The distance between the two points in the requested unit, as a float.
    Example :-

    >>> from turfpy import measurement
    >>> from geojson import Point
    >>> start = Point((-75.343, 39.984))
    >>> end = Point((-75.534, 39.123))
    >>> measurement.distance(start,end)

    """
    coordinates1 = get_coord(point1)
    coordinates2 = get_coord(point2)

    dLat = radians((coordinates2[1] - coordinates1[1]))

    dLon = radians((coordinates2[0] - coordinates1[0]))

    lat1 = radians(coordinates1[1])

    lat2 = radians(coordinates2[1])

    a = pow(sin(dLat / 2), 2) + pow(sin(dLon / 2), 2) * cos(lat1) * cos(lat2)
    b = 2 * atan2(sqrt(a), sqrt(1 - a))
    return radians_to_length(b, units)


# -------------------------------#

# ----------- Area --------------#

def area(geojson: Union[
    Point, LineString, Polygon, MultiPoint, MultiLineString, MultiPolygon, Feature, FeatureCollection]):
    """
    This function calculates the area of the Geojson object given as input.
    :param geojson: Geojson object for which area is to be found.
    :return: area for the given Geojson object.
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


def bbox(geojson):
    """
    This function is used to generate bounding box coordinates for given geojson.
    :param geojson: Geojson object for which bounding box is to be found.
    :return: bounding box for the given Geojson object.
    Example :-

    >>> from turfpy.measurement import bbox
    >>> from geojson import Polygon

    >>> p = Polygon([[(2.38, 57.322), (23.194, -20.28), (-120.43, 19.15), (2.38, 57.322)]])
    >>> bb = bbox(p)
    """
    result = [float('inf'), float('inf'), float('-inf'), float('-inf')]

    def callback_coord_each(coord, coord_index, feature_index, multi_feature_index, geometry_index):
        nonlocal result
        if result[0] > coord[0]:
            result[0] = coord[0]
        if result[1] > coord[1]:
            result[1] = coord[1]
        if result[2] < coord[0]:
            result[2] = coord[0]
        if result[3] < coord[1]:
            result[3] = coord[1]

    coord_each(geojson, callback_coord_each)
    return result


# -------------------------------#

# ----------- BBoxPolygon --------------#

def bbox_polygon(bbox: list, properties: dict = {}) -> Feature:
    """
    To generate a Polygon Feature for the bounding box generated using bbox.
    :param bbox: bounding box generated for a geojson.
    :param properties: properties to be added to the returned feature.
    :return: polygon for the given bounding box coordinates.
    Example :-
    >>> from turfpy.measurement import bbox_polygon, bbox
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
    Takes a Feature or FeatureCollection and returns the absolute center point of all features.
    :param geojson: GeoJSON for which centered to be calculated.
    :param properties: Optional parameters to be set to the generated feature.
    :return: Point feature for the center.
    Example :-
    >>> from turfpy.measurement import center
    >>> from geojson import Feature, FeatureCollection, Point

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
    Takes any number of features and returns a rectangular Polygon that encompasses all vertices.
    :param geojson: geojson input features for which envelope to be generated.
    :return: returns envelope i.e bounding box polygon.
    Example :-
    >>> from turfpy.measurement import envelope
    >>> from geojson import Feature, FeatureCollection, Point

    >>> f1 = Feature(geometry=Point((-97.522259, 35.4691)))
    >>> f2 = Feature(geometry=Point((-97.502754, 35.463455)))
    >>> f3 = Feature(geometry=Point((-97.508269, 35.463245)))
    >>> feature_collection = FeatureCollection([f1, f2, f3])
    >>> feature = envelope(feature_collection)
    """
    return bbox_polygon(bbox(geojson))


# -------------------------------#

# ----------- Length --------------#


def length(geojson, units: str = 'km'):
    """
    Takes a geojson and measures its length in the specified units.
    :param geojson: geojson for which the length is to be determined.
    :param units: units in which length is to be returned.
    :return: length of the geojson in specified units.
    Example:-
    >>> from turfpy.measurement import length
    >>> from geojson import LineString
    >>> ls = LineString([(115, -32), (131, -22), (143, -25), (150, -34)])
    >>> length(ls)
    """

    def callback_segment_reduce(previous_value, segment):
        coords = segment['geometry']['coordinates']
        return previous_value + distance(Point(coords[0]), Point(coords[1]), units)

    return segment_reduce(geojson, callback_segment_reduce, 0)


# -------------------------------#

# ----------- Destination --------------#

def destination(origin: Point, distance, bearing, options: dict = {}) -> Feature:
    """
    Takes a Point and calculates the location of a destination point given a distance in degrees, radians, miles,
    or kilometers and bearing in degrees.
    :param origin: Start point.
    :param distance: distance upto which the destination is from origin.
    :param bearing: Direction in which is the destination is from origin.
    :param options: Option like units of distance and properties to be passed to destination point feature, value
    for units are 'mi', 'km', 'deg' and 'rad'.
    :return: Feature: destination point in at the given distance and given direction.
    Example :-
    >>> from turfpy.measurement import destination
    >>> from geojson import Point
    >>> origin = Point([-75.343, 39.984])
    >>> distance = 50
    >>> bearing = 90
    >>> options = {'units': 'mi'}
    >>> destination(origin,distance,bearing,options)
    """
    coordinates1 = origin['coordinates']
    longitude1 = radians(float(coordinates1[0]))
    latitude1 = radians(float(coordinates1[1]))
    bearingRad = radians(float(bearing))
    if 'units' in options:
        radian = length_to_radians(distance, options['units'])
    else:
        radian = length_to_radians(distance)

    latitude2 = asin((sin(latitude1) * cos(radian)) + (cos(latitude1) * sin(radian) * cos(bearingRad)))
    longitude2 = longitude1 + atan2(sin(bearingRad) * sin(radian) * cos(latitude1),
                                    cos(radian) - sin(latitude1) * sin(latitude2))

    lng = degrees(longitude2)
    lat = degrees(latitude2)

    point = Point((lng, lat))

    return Feature(geometry=point, properties=options['properties'] if 'properties' in options else {})


# -------------------------------#

# ----------- Centroid --------------#

def centroid(geojson, properties: dict = None) -> Feature:
    """
    Takes one or more features and calculates the centroid using the mean of all vertices.
    :param geojson: Input features
    :param properties: Properties to be set to the output Feature point
    :return: Feature: Point feature which is the centroid of the given features
    Example:-
    >>> from turfpy.measurement import centroid
    >>> from geojson import Polygon
    >>> polygon = Polygon([[(-81, 41), (-88, 36), (-84, 31), (-80, 33), (-77, 39), (-81, 41)]])
    >>> centroid(polygon)
    """
    x_sum = 0
    y_sum = 0
    len = 0

    def callback_coord_each(coord, coord_index, feature_index, multi_feature_index, geometry_index):
        nonlocal x_sum, y_sum, len
        x_sum += coord[0]
        y_sum += coord[1]
        len += 1

    coord_each(geojson, callback_coord_each)
    point = Point((x_sum / len, y_sum / len))
    return Feature(geometry=point, properties=properties if properties else {})


# -------------------------------#

# ----------- Along --------------#

def along(line: Feature, dist, unit: str = 'km') -> Feature:
    """
    This function is used identify a Point at a specified distance along a LineString.
    :param line: LineString on which the point to be identified
    :param dist: Distance from the start of the LineString
    :param unit: unit of distance
    :return: Feature : Point at the distance on the LineString passed
    Example :-
    >>> from turfpy.measurement import along
    >>> from geojson import LineString
    >>> ls = LineString([(-83, 30), (-84, 36), (-78, 41)])
    >>> along(ls,200,'mi')
    """
    geom = ''
    if line['type'] == 'Feature':
        geom = line['geometry']
    else:
        geom = line

    coords = geom['coordinates']
    travelled = 0
    options = {'units': unit}
    for i in range(0, len(coords)):
        if dist >= travelled and i == (len(coords) - 1):
            break
        elif travelled >= dist:
            overshot = dist - travelled
            if not overshot:
                return Point(coords[i])
            else:
                direction = bearing(Point(coords[i]), Point(coords[i - 1])) - 180

                interpolated = destination(Point(coords[i]), overshot, direction, options)
                return interpolated
        else:

            travelled += distance(Point(coords[i]), Point(coords[i + 1]), unit)
    point = Point(coords[len(coords) - 1])

    return Feature(geometry=point)


# -------------------------------#

# ----------- Midpoint --------------#

def midpoint(point1: Point, point2: Point) -> Feature:
    """
    This function is used to get midpoint between any the two points.
    :param point1: First point.
    :param point2: Second point.
    :return: Feature: Point which is the midpoint of the two points given as input.
    Example:-
    >>> from turfpy.measurement import midpoint
    >>> from geojson import Point
    >>> point1 = Point([144.834823, -37.771257])
    >>> point2 = Point([145.14244, -37.830937])
    >>> midpoint(point1, point2)
    """
    dist = distance(point1, point2)
    heading = bearing(point1, point2)
    midpoint = destination(point1, dist / 2, heading)

    return midpoint


# -------------------------------#

# ----------- nearest point --------------#

def nearest_point(target_point: Feature, points: FeatureCollection) -> Feature:
    """
    Takes a reference Point Feature and FeatureCollection of point features and returns the point from the
    FeatureCollection closest to the reference Point Feature.
    :param target_point: Feature Point of reference.
    :param points: FeatureCollection of points.
    :return: a Point Feature from the FeatureCollection which is closest to the reference Point.
    Example:-
    >>> from turfpy.measurement import nearest_point
    >>> from geojson import Point, Feature, FeatureCollection
    >>> f1 = Feature(geometry=Point([28.96991729736328,41.01190001748873]))
    >>> f2 = Feature(geometry=Point([28.948459, 41.024204]))
    >>> f3 = Feature(geometry=Point([28.938674, 41.013324]))
    >>> fc = FeatureCollection([f1, f2 ,f3])
    >>> t = Feature(geometry=Point([28.973865, 41.011122]))
    >>> nearest_point(t ,fc)
    """
    if not target_point:
        raise Exception('target_point is required')

    if not points:
        raise Exception('points is required')

    min_dist = float('inf')
    nearest = ''
    best_feature_index = 0

    def callback_feature_each(pt, feature_index):
        nonlocal min_dist, best_feature_index
        distance_to_point = distance(target_point['geometry'], pt['geometry'])
        if float(distance_to_point) < min_dist:
            best_feature_index = feature_index
            min_dist = distance_to_point

    feature_each(points, callback_feature_each)

    nearest = points['features'][best_feature_index]
    nearest['properties']['featureIndex'] = best_feature_index
    nearest['properties']['distanceToPoint'] = min_dist
    return nearest


# -------------------------------#

# ----------- point on feature --------------#

def point_on_feature(geojson) -> Feature:
    """
    Takes a Feature or FeatureCollection and returns a Point guaranteed to be on the surface of the feature.
    :param geojson: Feature or FeatureCollection on which the Point is to be found.
    :return: Feature point which on the provided feature.
    Example:-
    >>> from turfpy.measurement import point_on_feature
    >>> from geojson import  Polygon, Feature
    >>> point = Polygon([[(116, -36), (131, -32), (146, -43), (155, -25), (133, -9), (111, -22), (116, -36)]])
    >>> feature = Feature(geometry=point)
    >>> point_on_feature(feature)
    """
    fc = normalize(geojson)

    cent = centroid(fc)

    on_surface = False
    i = 0
    while not on_surface and i < len(fc['features']):
        on_line = False
        geom = fc['features'][i]['geometry']
        if geom['type'] == 'Point':
            if cent['geometry']['coordinates'][0] == geom['coordinates'][0] and cent['geometry']['coordinates'][1] == \
                    geom['coordinates'][1]:
                on_surface = True
        elif geom['type'] == 'MultiPoint':
            on_multi_point = False
            k = 0
            while not on_multi_point and k < len(geom['coordinates']):
                if cent['geometry']['coordinates'][0] == geom['coordinates'][k][0] and cent['geometry']['coordinates'][
                    1] == geom['coordinates'][k][1]:
                    on_surface = True
                    on_multi_point = True
                k = k + 1
        elif geom['type'] == 'LineString':
            k = 0
            while not on_line and k < len(geom['coordinates']) - 1:
                x = cent['geometry']['coordinates'][0]
                y = cent['geometry']['coordinates'][1]
                x1 = geom['coordinates'][k][0]
                y1 = geom['coordinates'][k][1]
                x2 = geom['coordinates'][k + 1][0]
                y2 = geom['coordinates'][k + 1][1]
                if point_on_segment(x, y, x1, y1, x2, y2):
                    on_line = True
                    on_surface = True
                k = k + 1
        elif geom['type'] == 'MultiLineString':
            j = 0
            while j < len(geom['coordinates']):
                on_line = False
                k = 0
                line = geom['coordinates'][j]
                while not on_line and k < len(line) - 1:
                    x = cent['geometry']['coordinates'][0];
                    y = cent['geometry']['coordinates'][1]
                    x1 = line[k][0]
                    y1 = line[k][1]
                    x2 = line[k + 1][0]
                    y2 = line[k + 1][1]
                    if point_on_segment(x, y, x1, y1, x2, y2):
                        on_line = True
                        on_surface = True
                    k = k + 1
                j = j + 1
        elif geom['type'] == 'Polygon' or geom['type'] == 'MultiPolygon':
            if boolean_point_in_polygon(cent, geom):
                on_surface = True
        i = i + 1

    if on_surface:
        return cent
    else:
        vertices_list = []
        for i in range(0, len(fc['features'])):
            vertices_list.extend(explode(fc['features'][i])['features'])
        vertices = FeatureCollection(vertices_list)
        point = Point(nearest_point(cent, vertices)['geometry']['coordinates'])
        return Feature(geometry=point)


def normalize(geojson):
    if geojson['type'] != 'FeatureCollection':
        if geojson['type'] != 'Feature':
            return FeatureCollection([Feature(geometry=geojson)])
        return FeatureCollection([geojson])
    return geojson


def point_on_segment(x, y, x1, y1, x2, y2):
    ab = sqrt((x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1))
    ap = sqrt((x - x1) * (x - x1) + (y - y1) * (y - y1))
    pb = sqrt((x2 - x) * (x2 - x) + (y2 - y) * (y2 - y))
    return ab == (ap + pb)


# -------------------------------#

# ------------ boolean point in polygon ----------------#

def boolean_point_in_polygon(point, polygon, ignore_boundary=False):
    """
    Takes a Point or a Point Feature and Polygon or Polygon Feature as input and returns True if Point is in given
    Feature.
    :param point: Point or Point Feature.
    :param polygon: Polygon or Polygon Feature.
    :param ignore_boundary: [Optional] default value is False, specify whether to exclude boundary of the given polygon
    or not.
    :return: True if the given Point is in Polygons else False
    Example:-
    >>> from turfpy.measurement import boolean_point_in_polygon
    >>> from geojson import Point, MultiPolygon, Feature
    >>> point = Feature(geometry=Point([-77, 44]))
    >>> polygon = Feature(geometry=MultiPolygon([([(-81, 41), (-81, 47), (-72, 47), (-72, 41), (-81, 41)],),
    >>> ([(3.78, 9.28), (-130.91, 1.52), (35.12, 72.234), (3.78, 9.28)],)]))
    >>> boolean_point_in_polygon(point, polygon)
    """
    if not point: raise Exception('point is required')
    if not polygon: raise Exception('polygon is required')

    pt = get_coord(point)
    geom = get_geom(polygon)
    type = geom['type']
    bbox = polygon.get('bbox', None)
    polys = geom['coordinates']

    if bbox and not in_bbox(pt, bbox):
        return False

    if type == 'Polygon':
        polys = [polys]

    inside_poly = False

    for i in range(0, len(polys)):
        if in_ring(pt, polys[i][0], ignore_boundary):
            in_hole = False
            k = 1
            while k < len(polys[i]) and not in_hole:
                if in_ring(pt, polys[i][k], not ignore_boundary):
                    in_hole = True
                k = k + 1
            if not in_hole:
                inside_poly = True

    return inside_poly


def in_ring(pt, ring, ignore_boundary):
    is_inside = False
    if ring[0][0] == ring[len(ring) - 1][0] and ring[0][1] == ring[len(ring) - 1][1]:
        ring = ring[0:len(ring) - 1]
    j = len(ring) - 1
    for i in range(0, len(ring)):
        xi = ring[i][0]
        yi = ring[i][1]
        xj = ring[j][0]
        yj = ring[j][1]
        on_boundary = (pt[1] * (xi - xj) + yi * (xj - pt[0]) + yj * (pt[0] - xi) == 0) and \
                      ((xi - pt[0]) * (xj - pt[0]) <= 0) and ((yi - pt[1]) * (yj - pt[1]) <= 0)
        if on_boundary:
            return not ignore_boundary
        intersect = ((yi > pt[1]) != (yj > pt[1])) and \
                    (pt[0] < (xj - xi) * (pt[1] - yi) / (yj - yi) + xi)
        if intersect:
            is_inside = not is_inside
        j = i
    return is_inside


def in_bbox(pt, bbox):
    return bbox[0] <= pt[0] <= bbox[2] and \
           bbox[1] <= pt[1] <= bbox[3]


# -------------------------------#

# ------------ Explode -----------#

def explode(geojson):
    points = []
    if geojson['type'] == 'FeatureCollection':
        def callback_feature_each(feature, feature_index):
            def callback_coord_each(coord, coord_index, feature_index, multi_feature_index, geometry_index):
                nonlocal points
                point = Point(coord)
                points.append(Feature(geometry=point, properties=feature['properties']))

            coord_each(feature, callback_coord_each)

        feature_each(geojson, callback_feature_each)
    else:
        def callback_coord_each(coord, coord_index, feature_index, multi_feature_index, geometry_index):
            nonlocal points, geojson
            point = Point(coord)
            points.append(Feature(geometry=point, properties=geojson['properties']))

        coord_each(geojson, callback_coord_each)
    return FeatureCollection(points)


# -------------------------------#

# ------------ polygon tangents -----------#

def polygon_tangents(point, polygon):
    """
    Finds the tangents of a (Multi)Polygon from a Point.
    :param point: Point or Point Feature.
    :param polygon: (Multi)Polygon or (Multi)Polygon Feature.
    :return: FeatureCollection of two tangent Point Feature.
    Example:-
    >>> from turfpy.measurement import polygon_tangents
    >>> from geojson import Polygon, Point, Feature
    >>> point = Feature(geometry=Point([61, 5]))
    >>> polygon = Feature(geometry=Polygon([[(11, 0), (22, 4), (31, 0), (31, 11), (21, 15), (11, 11), (11, 0)]]))
    >>> polygon_tangents(point, polygon)
    """
    point_coords = get_coords(point)
    poly_coords = get_coords(polygon)

    enext = 0
    bbox_points = bbox(polygon)
    nearest_pt_index = 0
    nearest = None

    if point_coords[0] > bbox_points[0] and point_coords[0] < bbox_points[2] and point_coords[1] > bbox_points[1] and \
            point_coords[1] < bbox_points[3]:
        nearest = nearest_point(point, explode(polygon))
        nearest_pt_index = nearest.properties.featureIndex

    type = get_type(polygon)

    if type == 'Polygon':
        rtan = poly_coords[0][nearest_pt_index]
        ltan = poly_coords[0][0]
        if nearest:
            if nearest['geometry']['coordinates'][1] < point_coords[1]: ltan = poly_coords[0][nearest_pt_index]

        eprev = is_left(poly_coords[0][0], poly_coords[0][len(poly_coords[0]) - 1], point_coords)
        out = process_polygon(poly_coords[0], point_coords, eprev, enext, rtan, ltan)
        rtan = out[0]
        ltan = out[1]
    elif type == 'MultiPolygon':
        closest_feature = 0
        closest_vertex = 0
        vertices_counted = 0
        for i in range(0, len(poly_coords[0])):
            closest_feature = i
            vertice_found = False
            for i2 in range(0, len(poly_coords[0][i])):
                closest_vertex = i2
                if vertices_counted == nearest_pt_index:
                    vertice_found = True
                    break
                vertices_counted = vertices_counted + 1
            if vertice_found: break
        rtan = poly_coords[0][closest_feature][closest_vertex]
        ltan = poly_coords[0][closest_feature][closest_vertex]
        eprev = is_left(poly_coords[0][0][0], poly_coords[0][0][len(poly_coords[0][0]) - 1], point_coords)
        for ring in poly_coords:
            out = process_polygon(ring[0], point_coords, eprev, enext, rtan, ltan)
            rtan = out[0]
            ltan = out[1]

    return FeatureCollection([Feature(geometry=Point(rtan)), Feature(geometry=Point(ltan))])


def process_polygon(polygon_coords, pt_coords, eprev, enext, rtan, ltan):
    for i in range(0, len(polygon_coords)):
        current_coords = polygon_coords[i]
        if i == (len(polygon_coords) - 1):
            next_coord_pair = polygon_coords[0]
        else:
            next_coord_pair = polygon_coords[i + 1]
        enext = is_left(current_coords, next_coord_pair, pt_coords)
        if eprev <= 0 and enext > 0:
            if not is_below(pt_coords, current_coords, rtan):
                rtan = current_coords
        elif eprev > 0 and enext <= 0:
            if not is_above(pt_coords, current_coords, ltan):
                ltan = current_coords
        eprev = enext
    return [rtan, ltan]


def is_above(point1, point2, point3):
    return is_left(point1, point2, point3) > 0


def is_below(point1, point2, point3):
    return is_left(point1, point2, point3) < 0


def is_left(point1, point2, point3):
    return (point2[0] - point1[0]) * (point3[1] - point1[1]) - (point3[0] - point1[0]) * (point2[1] - point1[1])


# -------------------------------#

# ------------ point to line distance -----------#

def point_to_line_distance(point: Feature, line: Feature, units='km', method='geodesic'):
    """
    Returns the minimum distance between a Point and any segment of the LineString.
    :param point: Point Feature from which distance to be measured.
    :param line: Point LineString from which distance to be measured.
    :param units: units for distance 'km', 'm', 'mi, 'ft', 'in', 'deg', 'cen', 'rad', 'naut', 'yd'
    :param method: Method which is used to calculate, values can be 'geodesic' or 'planar'
    :return: Approximate distance between the LineString and Point
    Example:-
    >>> from turfpy.measurement import point_to_line_distance
    >>> from geojson import LineString, Point, Feature
    >>> point = Feature(geometry=Point([0, 0]))
    >>> linestring = Feature(geometry=LineString([(1, 1),(-1, 1)]))
    >>> point_to_line_distance(point, linestring)
    """
    if method != 'geodesic' and method != 'planar':
        raise Exception('method name is incorrect ot should be either geodesic or planar')

    options = {'units': units, 'method': method}

    if not point:
        raise Exception('pt is required')

    if isinstance(point, list):
        point = Feature(geometry=Point(point))
    elif point['type'] == 'Point':
        point = Feature(point)
    else:
        feature_of(point, 'Point', 'point')

    if not line:
        raise Exception('line is required')

    if isinstance(point, list):
        line = Feature(geometry=LineString(line))
    elif line['type'] == 'LineString':
        line = Feature(geometry=line)
    else:
        feature_of(line, 'LineString', 'line')

    distance = float('inf')

    p = point['geometry']['coordinates']

    def callback_segment_each(current_segment, feature_index, multi_feature_index, geometry_index, segment_index):
        nonlocal options, distance
        a = current_segment['geometry']['coordinates'][0]
        b = current_segment['geometry']['coordinates'][1]
        d = distance_to_segment(p, a, b, options)
        if d < distance:
            distance = d

    segment_each(line, callback_segment_each)

    return convert_length(distance, 'deg', options.get('units', ''))


def distance_to_segment(p, a, b, options):
    v = [b[0] - a[0], b[1] - a[1]]
    w = [p[0] - a[0], p[1] - a[1]]

    c1 = dot(w, v)
    if c1 <= 0:
        return calc_distance(p, a, {'method': options.get('method', ''), 'units': "deg"})
    c2 = dot(v, v)
    if c2 <= c1:
        return calc_distance(p, b, {'method': options.get('method', ''), 'units': "deg"})
    b2 = c1 / c2
    Pb = [a[0] + (b2 * v[0]), a[1] + (b2 * v[1])]

    return calc_distance(p, Pb, {'method': options.get('method', ''), 'units': "deg"})


def calc_distance(a, b, options):
    if options.get('method', '') == 'planar':
        return rhumb_distance(a, b, options.get('units', ''))
    else:
        return distance(a, b, options.get('units', ''))


def dot(u, v):
    return u[0] * v[0] + u[1] * v[1]


# -------------------------------#

# ------------ rhumb bearing -----------#

def rhumb_bearing(start, end, final=False):
    """
    Takes two points and finds the bearing angle between them along a Rhumb line i.e. the angle measured in degrees start the north line (0 degrees).
    :param start: Start Point or Point Feature.
    :param end: End Point or Point Feature.
    :param final: Calculates the final bearing if true
    :return: bearing from north in decimal degrees, between -180 and 180 degrees (positive clockwise)
    Example:-
    >>> from turfpy.measurement import rhumb_bearing
    >>> from geojson import Feature, Point
    >>> start = Feature(geometry=Point([-75.343, 39.984]))
    >>> end = Feature(geometry=Point([-75.534, 39.123]))
    >>> rhumb_bearing(start, end, True)
    """
    if final:
        bear_360 = calculate_rhumb_bearing(get_coord(end), get_coord(start))
    else:
        bear_360 = calculate_rhumb_bearing(get_coord(start), get_coord(end))

    if bear_360 > 180:
        bear_180 = -1 * (360 - bear_360)
    else:
        bear_180 = bear_360

    return bear_180


def calculate_rhumb_bearing(fro, to):
    phi1 = radians(fro[1])
    phi2 = radians(to[1])
    delta_lambda = radians(to[0] - fro[0])

    if delta_lambda > pi:
        delta_lambda -= (2 * pi)
    if delta_lambda < -1 * (pi):
        delta_lambda += (2 * pi)

    delta_psi = log(tan(phi2 / 2 + pi / 4) / tan(phi1 / 2 + pi / 4))

    theta = atan2(delta_lambda, delta_psi)

    return (degrees(theta) + 360) % 360


# -------------------------------#

# ------------ rhumb destination -----------#

def rhumb_destination(origin, distance, bearing, options) -> Feature:
    """
    Returns the destination Point having travelled the given distance along a Rhumb line from the origin Point with the (varant) given bearing.
    :param origin: Starting Point
    :param distance: Distance from the starting point
    :param bearing: Varant bearing angle ranging from -180 to 180 degrees from north
    :param options: A dict of two values 'units' for the units of distance provided and 'properties' that are to be
    passed to the Destination Feature Point Example :- {'units':'mi', 'properties': {"marker-color": "F00"}}
    :return: Destination Feature Point
    Example:-
    >>> from turfpy.measurement import rhumb_destination
    >>> from geojson import Point, Feature
    >>> start = Feature(geometry=Point([-75.343, 39.984]), properties={"marker-color": "F00"})
    >>> distance = 50
    >>> bearing = 90
    >>> rhumb_destination(start, distance, bearing, {'units':'mi', 'properties': {"marker-color": "F00"}})
    """
    was_negative_distance = distance < 0
    distance_in_meters = convert_length(abs(distance), options.get('units', ''), 'm')
    if was_negative_distance:
        distance_in_meters = -1 * (abs(distance_in_meters))
    coords = get_coord(origin)
    destination_point = calculate_rhumb_destination(coords, distance_in_meters, bearing)
    return Feature(geometry=Point(destination_point), properties=options.get('properties', ''))


def calculate_rhumb_destination(origin, distance, bearing, radius=None):
    if not radius:
        radius = avg_earth_radius_km

    delta = distance / radius
    lambda1 = origin[0] * pi / 180
    phi1 = radians(origin[1])
    theta = radians(bearing)
    delta_phi = delta * cos(theta)
    phi2 = phi1 + delta_phi

    if abs(phi2) > pi / 2:
        if phi2 > 0:
            phi2 = pi - phi2
        else:
            phi2 = -1 * pi - phi2

    delta_psi = log(tan(phi2 / 2 + pi / 4) / tan(phi1 / 2 + pi / 4))

    if abs(delta_psi) > 10e-12:
        q = delta_phi / delta_psi
    else:
        q = cos(phi1)

    delta_lambda = delta * sin(theta) / q

    lambda2 = lambda1 + delta_lambda

    return [((lambda2 * 180 / pi) + 540) % 360 - 180, phi2 * 180 / pi]


# -------------------------------#

# ------------ rhumb distance -----------#

def rhumb_distance(start, to, units='km'):
    """
    Calculates the distance along a rhumb line between two points in degrees, radians, miles, or kilometers.
    :param start: Start Point or Point Feature from which distance to be calculated.
    :param to: End Point or Point Feature upto which distance to be calculated.
    :param units: Units in which distance to be calculated, values can be 'deg', 'rad', 'mi', 'km'
    :return: Distance calculated from provided start to end Point.
    Example:-
    >>> from turfpy.measurement import rhumb_distance
    >>> from geojson import Point, Feature
    >>> start = Feature(geometry=Point([-75.343, 39.984]))
    >>> end = Feature(geometry=Point([-75.534, 39.123]))
    >>> rhumb_distance(start, end,'mi')
    """
    origin = get_coord(start)
    destination = get_coord(to)

    if destination[0] - origin[0] > 180:
        temp = -360
    elif origin[0] - destination[0] > 180:
        temp = 360
    else:
        temp = 0
    destination[0] += temp

    distance_in_meters = calculate_rhumb_distance(origin, destination)
    ru_distance = convert_length(distance_in_meters, 'm', units)
    return ru_distance


def calculate_rhumb_distance(origin, destination_point, radius=None):
    if not radius:
        radius = avg_earth_radius_km
    R = radius
    phi1 = origin[1] * pi / 180
    phi2 = destination_point[1] * pi / 180
    delta_phi = phi2 - phi1
    delta_lambda = abs(destination_point[0] - origin[0]) * pi / 180

    if delta_lambda > pi:
        delta_lambda -= 2 * pi

    delta_psi = log(tan(phi2 / 2 + pi / 4) / tan(phi1 / 2 + pi / 4))
    if abs(delta_psi) > 10e-12:
        q = delta_phi / delta_psi
    else:
        q = cos(phi1)

    delta = sqrt(delta_phi * delta_phi + q * q * delta_lambda * delta_lambda)
    dist = delta * R

    return dist


# -------------------------------#

# ------------ square -----------#

def square(bbox: list):
    """
    Takes a bounding box and calculates the minimum square bounding box that would contain the input.
    :param bbox: Bounding box extent in west, south, east, north order
    :return: A square surrounding bbox
    Example:-
    >>> from turfpy.measurement import square
    >>> bbox = [-20, -20, -15, 0]
    >>> square(bbox)
    """
    west = bbox[0]
    south = bbox[1]
    east = bbox[2]
    north = bbox[3]

    horizontal_distance = distance(bbox[0:2], [east, south])
    vertical_distance = distance(bbox[0:2], [west, north])
    if horizontal_distance >= vertical_distance:
        vertical_midpoint = (south + north) / 2
        return [
            west,
            vertical_midpoint - ((east - west) / 2),
            east,
            vertical_midpoint + ((east - west) / 2)
        ]
    else:
        horizontal_midpoint = (west + east) / 2;
        return [
            horizontal_midpoint - ((north - south) / 2),
            south,
            horizontal_midpoint + ((north - south) / 2),
            north
        ]

# -------------------------------#

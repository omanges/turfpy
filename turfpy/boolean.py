"""
This module implements some of the spatial analysis techniques and processes used to
understand the patterns and relationships of geographic features.
This is mainly inspired by turf.js.
link: http://turfjs.org/
"""

from geojson import Feature, Point, LineString, Polygon

from turfpy.meta import flatten_each
from turfpy.misc import line_intersect
from turfpy.measurement import boolean_point_in_polygon
from turfpy.feature_conversion import polygon_to_line

def __is_point_on_line(
    line_string: LineString,
    point: Point
) -> bool:
    """
    Determine if point is on a line

    :param line_string: GeoJSON LineString
    :type line_string: LineString
    :param point: GeoJSON Point
    :type point: Point
    :returns: True if the point is on the line
    :rtype: bool
    """
    coordinates = line_string['coordinates']
    pt_coordinates = point['coordinates']
    
    for i in range(len(coordinates) - 1):
        if __is_point_on_line_segment(coordinates[i], coordinates[i + 1], pt_coordinates):
            return True
    return False

def __is_line_on_line(
    line_string_1: LineString,
    line_string_2: LineString
) -> bool:
    """
    Determine if line is on line

    :param line_string_1: GeoJSON LineString
    :type line_string_1: LineString
    :param line_string_2: GeoJSON LineString
    :type line_string_2: LineString
    :returns: True if the line is on the other line
    :rtype: bool
    """
    do_lines_intersect = line_intersect(line_string_1, line_string_2)
    
    if len(do_lines_intersect['features']) > 0:
        return True
    return False

def __is_line_in_poly(
    polygon: Polygon,
    line_string: LineString
) -> bool:
    """
    Determine if line is in a polygon


    :param polygon: GeoJSON Polygon
    :type polygon: Polygon
    :param line_string: GeoJSON LineString
    :type line_string: LineString
    :returns: True if the line is in the polygon
    :rtype: bool
    """
    for coord in line_string['coordinates']:
        if boolean_point_in_polygon(coord, polygon):
            return True
    
    do_lines_intersect = line_intersect(line_string, polygon_to_line(polygon))
    
    if len(do_lines_intersect['features']) > 0:
        return True
    
    return False

def __is_poly_in_poly(
    feature1: Polygon,
    feature2: Polygon
) -> bool:
    """
    Determine if a polygon is in another polygon

    :param feature1: GeoJSON Polygon
    :type feature1: Polygon
    :param feature2: GeoJSON Polygon
    :type feature2: Polygon
    :returns: True if the polygon is in the other polygon
    :rtype: bool
    """
    for coord1 in feature1['coordinates'][0]:
        if boolean_point_in_polygon(coord1, feature2):
            return True
    
    for coord2 in feature2['coordinates'][0]:
        if boolean_point_in_polygon(coord2, feature1):
            return True
    
    do_lines_intersect = line_intersect(
        polygon_to_line(feature1),
        polygon_to_line(feature2)
    )
    
    if len(do_lines_intersect['features']) > 0:
        return True
    
    return False

def __is_point_on_line_segment(
    line_segment_start: list,
    line_segment_end: list,
    point: list
) -> bool:
    """
    Determine if point is on a line segment

    :param line_segment_start: start of line segment
    :type line_segment_start: list
    :param line_segment_end: end of line segment
    :type line_segment_end: list
    :param point: point to check
    :type point: list
    :returns: True if point is on the line segment
    :rtype: bool
    """

    dxc = point[0] - line_segment_start[0]
    dyc = point[1] - line_segment_start[1]
    dxl = line_segment_end[0] - line_segment_start[0]
    dyl = line_segment_end[1] - line_segment_start[1]
    cross = dxc * dyl - dyc * dxl
    
    if cross != 0:
        return False
    
    if abs(dxl) >= abs(dyl):
        if dxl > 0:
            return line_segment_start[0] <= point[0] <= line_segment_end[0]
        else:
            return line_segment_end[0] <= point[0] <= line_segment_start[0]
    else:
        if dyl > 0:
            return line_segment_start[1] <= point[1] <= line_segment_end[1]
        else:
            return line_segment_end[1] <= point[1] <= line_segment_start[1]

def __compare_coords(
    pair1: list,
    pair2: list
) -> bool:
    """
    Compare coordinates to see if they match

    :param pair1: pair of coordinates
    :type pair1: list
    :param pair2: pair of coordinates
    :type pair2: list
    :returns: True if the two pairs of coordinates match
    :rtype: bool
    """

    return pair1[0] == pair2[0] and pair1[1] == pair2[1]

def __disjoint(
    feature_1: Feature,
    feature_2: Feature
) -> bool:
    """
    Disjoint operation for simple Geometries (Point/LineString/Polygon)

    :param feature_1: GeoJSON Feature or Geometry
    :type feature_1: Feature
    :param feature_2: GeoJSON Feature or Geometry
    :type feature_2: Feature
    :param ignore_self_intersections: whether to ignore self intersections
    :type ignore_self_intersections: bool
    :returns: True if the two geometries do not touch or overlap.
    :rtype: bool 
    """

    geom1_type = feature_1['geometry']['type']
    geom2_type = feature_2['geometry']['type']
    
    if geom1_type == "Point":
        if geom2_type == "Point":
            return not __compare_coords(feature_1['geometry']['coordinates'], feature_2['geometry']['coordinates'])
        elif geom2_type == "LineString":
            return not __is_point_on_line(feature_2['geometry'], feature_1['geometry'])
        elif geom2_type == "Polygon":
            return not boolean_point_in_polygon(feature_1['geometry'], feature_2['geometry'])
    
    elif geom1_type == "LineString":
        if geom2_type == "Point":
            return not __is_point_on_line(feature_1['geometry'], feature_2['geometry'])
        elif geom2_type == "LineString":
            return not __is_line_on_line(feature_1['geometry'], feature_2['geometry'])
        elif geom2_type == "Polygon":
            return not __is_line_in_poly(feature_2['geometry'], feature_1['geometry'])
    
    elif geom1_type == "Polygon":
        if geom2_type == "Point":
            return not boolean_point_in_polygon(feature_2['geometry'], feature_1['geometry'])
        elif geom2_type == "LineString":
            return not __is_line_in_poly(feature_1['geometry'], feature_2['geometry'])
        elif geom2_type == "Polygon":
            return not __is_poly_in_poly(feature_2['geometry'], feature_1['geometry'])
    
    return False

def boolean_disjoint(
    feature_1: Feature, 
    feature_2: Feature
) -> bool:
    """
    Boolean-disjoint returns (TRUE) if the two geometries do not touch or overlap.

    :param feature_1: GeoJSON Feature or Geometry
    :type feature_1: Feature
    :param feature_2: GeoJSON Feature or Geometry
    :type feature_2: Feature
    :returns: True if the two geometries do not touch or overlap.
    :rtype: bool


    Example:

    >>> from turfpy.boolean import boolean_disjoint
    >>> from geojson import Feature, Polygon
    >>> boolean_disjoint()

    """

    bool_result = True
    
    def check_disjoint(flatten1, index1, feature_collection1):
        nonlocal bool_result
        if not bool_result:
            return False
        def inner_check(flatten2, index2, feature_collection2):
            nonlocal bool_result
            if not bool_result:
                return False
            bool_result = __disjoint(flatten1, flatten2)
        flatten_each(feature_2, inner_check)
    
    flatten_each(feature_1, check_disjoint)

    return bool_result

def boolean_intersects(
    feature_1: Feature, 
    feature_2: Feature
) -> bool:
    """
    Boolean-intersects returns (TRUE) if the intersection of the two geometries is NOT an empty set.

    :param feature_1: GeoJSON Feature or Geometry
    :type feature_1: Feature
    :param feature_2: GeoJSON Feature or Geometry
    :type feature_2: Feature
    :returns: True if the intersection of the two geometries is NOT an empty set.
    :rtype: bool
    """

    bool_result = False
    
    def check_intersection(flatten1, index1, feature_collection1):
        nonlocal bool_result
        if bool_result:
            return True
        def inner_check(flatten2, index2, feature_collection2):
            nonlocal bool_result
            if bool_result:
                return True
            bool_result = not boolean_disjoint(flatten1['geometry'], flatten2['geometry'])
        flatten_each(feature_2, inner_check)
    
    flatten_each(feature_1, check_intersection)

    return bool_result
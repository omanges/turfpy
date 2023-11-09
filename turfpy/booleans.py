"""
This module implements some of the spatial analysis techniques and processes used to
understand the patterns and relationships of geographic features.
This is mainly inspired by turf.js.
link: http://turfjs.org/
"""

from geojson import Polygon, LineString, Point, MultiPoint

from turfpy.measurement import (
    boolean_point_in_polygon,
    boolean_point_on_line
)

def boolean_within(feature1, feature2):
    geom1 = feature1['geometry'] if 'geometry' in feature1 else feature1
    geom2 = feature2['geometry'] if 'geometry' in feature2 else feature2
    type1 = geom1['type']
    type2 = geom2['type']

    switch_type1 = {
        "Point": lambda: {
            "MultiPoint": lambda: is_point_in_multi_point(geom1, geom2),
            "LineString": lambda: boolean_point_on_line(geom1, geom2, ignore_end_vertices=True),
            "Polygon": lambda: boolean_point_in_polygon(geom1, geom2, ignore_boundary=True),
            "MultiPolygon": lambda: boolean_point_in_polygon(geom1, geom2, ignore_boundary=True)
        },
        "MultiPoint": lambda: {
            "MultiPoint": lambda: is_multi_point_in_multi_point(geom1, geom2),
            "LineString": lambda: is_multi_point_on_line(geom1, geom2),
            "Polygon": lambda: is_multi_point_in_poly(geom1, geom2),
            "MultiPolygon": lambda: is_multi_point_in_poly(geom1, geom2)
        },
        "LineString": lambda: {
            "LineString": lambda: is_line_on_line(geom1, geom2),
            "Polygon": lambda: is_line_in_poly(geom1, geom2),
            "MultiPolygon": lambda: is_line_in_poly(geom1, geom2)
        },
        "Polygon": lambda: {
            "Polygon": lambda: is_poly_in_poly(geom1, geom2),
            "MultiPolygon": lambda: is_poly_in_poly(geom1, geom2)
        }
    }

    return switch_type1.get(type1, lambda: f"feature1 {type1} geometry not supported")()[type2]()

def is_point_in_multi_point(point: Point, multi_point: MultiPoint):
    for p in multi_point['coordinates']:
        if p == point['coordinates']:
            return True
    return False

def is_multi_point_in_multi_point(multi_point1: MultiPoint, multi_point2: MultiPoint):
    for p1 in multi_point1['coordinates']:
        any_match = False
        for p2 in multi_point2['coordinates']:
            if p1 == p2:
                any_match = True
        if not any_match:
            return False
    return True

def is_multi_point_on_line(multi_point: LineString, line_string: LineString):
    found_inside_point = False
    for p in multi_point['coordinates']:
        if not boolean_point_on_line(p, line_string):
            return False
        if not found_inside_point:
            found_inside_point = boolean_point_on_line(p, line_string, {"ignore_end_vertices":True})
    return found_inside_point

def is_multi_point_in_poly(multi_point: MultiPoint, polygon: Polygon):
    output = True
    one_inside = False
    is_inside = False
    for p in multi_point['coordinates']:
        is_inside = boolean_point_in_polygon(p, polygon)
        if not is_inside:
            output = False
            break
        if not one_inside:
            is_inside = boolean_point_in_polygon(p, polygon, ignore_boundary=True)
    return output and is_inside

def is_line_on_line(line_string1: LineString, line_string2: LineString):
    for p in line_string1['coordinates']:
        if not boolean_point_on_line(p, line_string2):
            return False
    return True

def is_line_in_poly(linestring: LineString, polygon: Polygon):
    poly_bbox = calc_bbox(polygon)
    line_bbox = calc_bbox(linestring)
    if not do_bbox_overlap(poly_bbox, line_bbox):
        return False
    found_inside_point = False
    for i in range(len(linestring['coordinates']) - 1):
        if not boolean_point_in_polygon(linestring['coordinates'][i], polygon):
            return False
        if not found_inside_point:
            found_inside_point = boolean_point_in_polygon(
                linestring['coordinates'][i],
                polygon,
                ignore_boundary=True
            )
        if not found_inside_point:
            midpoint = get_midpoint(
                linestring['coordinates'][i],
                linestring['coordinates'][i + 1]
            )
            found_inside_point = boolean_point_in_polygon(
                midpoint,
                polygon,
                ignore_boundary=True
            )
    return found_inside_point

def is_poly_in_poly(geometry1: Polygon, geometry2: Polygon):
    poly1_bbox = calc_bbox(geometry1)
    poly2_bbox = calc_bbox(geometry2)
    if not do_bbox_overlap(poly2_bbox, poly1_bbox):
        return False
    for p in geometry1['coordinates'][0]:
        if not boolean_point_in_polygon(p, geometry2):
            return False
    return True

def calc_bbox(geometry):
    if geometry['type'] == "LineString":
        coordinates = geometry['coordinates']
    if geometry['type'] == "Polygon":
        coordinates = geometry['coordinates'][0]
    bbox = [float('inf'), float('inf'), float('-inf'), float('-inf')]
    for coords in coordinates:
        if bbox[0] > coords[0]:
            bbox[0] = coords[0]
        if bbox[1] > coords[1]:
            bbox[1] = coords[1]
        if bbox[2] < coords[0]:
            bbox[2] = coords[0]
        if bbox[3] < coords[1]:
            bbox[3] = coords[1]
    return bbox

def do_bbox_overlap(bbox1, bbox2):
    if bbox1[0] > bbox2[0]:
        return False
    if bbox1[2] < bbox2[2]:
        return False
    if bbox1[1] > bbox2[1]:
        return False
    if bbox1[3] < bbox2[3]:
        return False
    return True

def get_midpoint(pair1, pair2):
    x1, y1 = pair1
    x2, y2 = pair2
    return [(x1 + x2) / 2, (y1 + y2) / 2]

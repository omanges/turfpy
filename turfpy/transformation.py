"""
This module implements some of the spatial analysis techniques and processes used to
understand the patterns and relationships of geographic features.
This is mainly inspired by turf.js.
link: http://turfjs.org/
"""
import math
from math import floor
from typing import List, Union

import numpy as np
import shapely.geometry as geometry
from geojson import Feature, FeatureCollection, LineString, Polygon
from scipy.spatial import Delaunay
from shapely.geometry import Point, mapping, shape
from shapely.ops import cascaded_union, polygonize

from turfpy.helper import get_geom
from turfpy.measurement import bbox_polygon, destination

from .dev_lib.spline import Spline


def circle(
    center: Feature, radius: int, steps: int = 64, units: str = "km", **kwargs
) -> Polygon:
    """
    Takes a Point and calculates the circle polygon given a radius in degrees,
    radians, miles, or kilometers; and steps for precision.

    :param center: A `Point` object representing center point of circle.
    :param radius: An int representing radius of the circle.
    :param steps: An int representing number of steps.
    :param units: A string representing units of distance e.g. 'mi', 'km',
        'deg' and 'rad'.
    :param kwargs: A dict representing additional properties.
    :return: A polygon feature object.

    Example:

    >>> from turfpy.transformation import circle
    >>> from geojson import Feature, Point
    >>> circle(center=Feature(geometry=Point((-75.343, 39.984))), radius=5, steps=10)

    """
    coordinates = []
    options = dict(steps=steps, units=units)
    options.update(kwargs)
    for i in range(steps):
        bearing = i * -360 / steps
        pt = destination(center, radius, bearing, options=options)
        cords = pt.geometry.coordinates
        coordinates.append(cords)
    coordinates.append(coordinates[0])
    return Feature(geometry=Polygon([coordinates], **kwargs))


def bbox_clip(geojson: Feature, bbox: list):
    """
    Takes a Feature or geometry and a bbox and clips the feature to the bbox
    :param geojson: Geojson data
    :param bbox: Bounding Box which is used to clip the geojson
    :return: Clipped geojson

    Example:

    >>> from turfpy.transformation import bbox_clip
    >>> from geojson import Feature
    >>> f = Feature(geometry={"coordinates": [[[2, 2], [8, 4],
    >>> [12, 8], [3, 7], [2, 2]]], "type": "Polygon"})
    >>> bbox = [0, 0, 10, 10]
    >>> clip = bbox_clip(f, bbox)
    """
    bb_polygon = bbox_polygon(bbox)

    bb_clip = intersect([geojson, bb_polygon])

    if not bb_clip:
        return bb_clip

    if "properties" in geojson:
        bb_clip.properties = geojson["properties"]

    return bb_clip


def intersect(features) -> Feature:
    """
    Takes two polygons and finds their intersection
    :param features: List of features of Feature Collection
    :return: Intersection Geojson Feature

    Example:

    >>> from turfpy.transformation import intersect
    >>> from geojson import Feature
    >>> f = Feature(geometry={"coordinates": [
    >>> [[-122.801742, 45.48565], [-122.801742, 45.60491],
    >>> [-122.584762, 45.60491], [-122.584762, 45.48565],
    >>> [-122.801742, 45.48565]]], "type": "Polygon"})
    >>> b = Feature(geometry={"coordinates": [
    >>> [[-122.520217, 45.535693], [-122.64038, 45.553967],
    >>> [-122.720031, 45.526554], [-122.669906, 45.507309],
    >>> [-122.723464, 45.446643], [-122.532577, 45.408574],
    >>> [-122.487258, 45.477466], [-122.520217, 45.535693]
    >>> ]], "type": "Polygon"})
    >>> inter = intersect([f, b])
    """
    if isinstance(features, list):
        shapes = []
        for f in features:
            poly = get_geom(f)
            s = shape(poly)
            shapes.append(s)

    else:
        if "features" not in features.keys():
            raise Exception("Invalid FeatureCollection")
        shapes = []
        for f in features["features"]:
            poly = get_geom(f)
            s = shape(poly)
            shapes.append(s)

    intersection = shapes[0]

    for shape_value in shapes:
        intersection = shape_value.intersection(intersection)

    intersection = mapping(intersection)

    if len(intersection["coordinates"]) == 0:
        return None

    intersection_feature = Feature(geometry=intersection)

    return intersection_feature


def bezie_spline(line: Feature, resolution=10000, sharpness=0.85):
    """
    Takes a line and returns a curved version by applying a Bezier spline algorithm
    :param line: LineString Feature which is used to draw the curve
    :param resolution: time in milliseconds between points
    :param sharpness: a measure of how curvy the path should be between splines
    :return: Curve as LineString Feature

    Example:

    >>> from geojson import LineString, Feature
    >>> from turfpy.transformation import bezie_spline
    >>> ls = LineString([(-76.091308, 18.427501),
    >>>                     (-76.695556, 18.729501),
    >>>                     (-76.552734, 19.40443),
    >>>                     (-74.61914, 19.134789),
    >>>                     (-73.652343, 20.07657),
    >>>                     (-73.157958, 20.210656)])
    >>> f = Feature(geometry=ls)
    >>> bezie_spline(f)
    """
    coords = []
    points = []
    geom = get_geom(line)

    for c in geom["coordinates"]:
        points.append({"x": c[0], "y": c[1]})

    spline = Spline(points_data=points, resolution=resolution, sharpness=sharpness)

    i = 0
    while i < spline.duration:
        pos = spline.pos(i)
        if floor(i / 100) % 2 == 0:
            coords.append((pos["x"], pos["y"]))
        i = i + 10

    return Feature(geometry=LineString(coords))


def union(
    features: Union[List[Feature], FeatureCollection]
) -> Union[Feature, FeatureCollection]:
    """
    Given list of features or ``FeatureCollectio`` return union of those.

    :param features: A list of GeoJSON features or FeatureCollection.
    :return: A GeoJSON Feature or FeatureCollection.
    """

    shapes = []
    if isinstance(features, list):
        for f in features:
            if f.type != "Feature":
                raise Exception("Not a valid feature")
            geom = get_geom(f)
            s = shape(geom)
            shapes.append(s)
    else:
        if "features" not in features.keys():
            raise Exception("Invalid FeatureCollection")
        for f in features["features"]:
            geom = get_geom(f)
            s = shape(geom)
            shapes.append(s)

    result = cascaded_union(shapes)
    result = mapping(result)

    if result["type"] == "GeometryCollection":
        features = []
        for geom in result["geometries"]:
            features.append(Feature(geometry=geom))
        return FeatureCollection(features)

    return Feature(geometry=result)


def _alpha_shape(points, alpha):
    """
    Compute the alpha shape (concave hull) of a set of points.

    @param points: Iterable container of points.
    @param alpha: alpha value to influence the gooeyness of the border. Smaller
                  numbers don't fall inward as much as larger numbers. Too large,
                  and you lose everything!
    """
    if len(points) < 4:
        # When you have a triangle, there is no sense in computing an alpha
        # shape.
        return geometry.MultiPoint(list(points)).convex_hull

    def add_edge(edges, edge_points, coords, i, j):
        """Add a line between the i-th and j-th points, if not in the list already"""
        if (i, j) in edges or (j, i) in edges:
            # already added
            return
        edges.add((i, j))
        edge_points.append(coords[[i, j]])

    coords = np.array([point.coords[0] for point in points])

    tri = Delaunay(coords)
    edges = set()
    edge_points = []
    # loop over triangles:
    # ia, ib, ic = indices of corner points of the triangle
    for ia, ib, ic in tri.vertices:
        pa = coords[ia]
        pb = coords[ib]
        pc = coords[ic]

        # Lengths of sides of triangle
        a = math.sqrt((pa[0] - pb[0]) ** 2 + (pa[1] - pb[1]) ** 2)
        b = math.sqrt((pb[0] - pc[0]) ** 2 + (pb[1] - pc[1]) ** 2)
        c = math.sqrt((pc[0] - pa[0]) ** 2 + (pc[1] - pa[1]) ** 2)

        # Semiperimeter of triangle
        s = (a + b + c) / 2.0

        # Area of triangle by Heron's formula
        area = math.sqrt(s * (s - a) * (s - b) * (s - c))
        circum_r = a * b * c / (4.0 * area)

        # Here's the radius filter.
        # print circum_r
        if circum_r < 1.0 / alpha:
            add_edge(edges, edge_points, coords, ia, ib)
            add_edge(edges, edge_points, coords, ib, ic)
            add_edge(edges, edge_points, coords, ic, ia)

    m = geometry.MultiLineString(edge_points)
    triangles = list(polygonize(m))
    return cascaded_union(triangles), edge_points


def get_points(features):
    points = []
    if "type" not in features.keys():
        raise Exception("Invalid Feature")

    if features["type"] == "Feature":
        get_ext_points(geometry.shape(features["geometry"]), points)
    else:
        if "features" not in features.keys():
            raise Exception("Invalid FeatureCollection")

        for feature in features["features"]:
            get_ext_points(geometry.shape(feature["geometry"]), points)
    return points


def get_ext_points(geom, points):
    if geom.type == "Point":
        for p in geom.coords:
            points.append(Point(p))
    elif geom.type == "MultiPoint":
        for p in geom.geoms:
            points.append(p)
    elif geom.type == "LineString":
        for p in geom.coords:
            points.append(Point(p))
    elif geom.type == "MultiLineString":
        for g in geom.geoms:
            for p in g.coords:
                points.append(Point(p))
    elif geom.type == "Polygon":
        for p in geom.exterior.coords:
            points.append(Point(p))
    elif geom.type == "MultiPolygon":
        for g in geom.geoms:
            for p in g.exterior.coords:
                points.append(Point(p))
    else:
        raise Exception("Invalid Geometry")


def concave(features: FeatureCollection, alpha=2):
    """
    Generate concave hull for the given feature or Feature Collection
    :param features: It can be a feature or Feature Collection
    :param alpha: Alpha determines the shape of concave hull,
            greater values will make shape more tighten
    :return: Feature of concave hull polygon

    Example:
    >>> from turfpy.transformation import concave
    >>> from geojson import FeatureCollection, Feature, Point
    >>> f1 = Feature(geometry=Point((-63.601226, 44.642643)))
    >>> f2 = Feature(geometry=Point((-63.591442, 44.651436)))
    >>> f3 = Feature(geometry=Point((-63.580799, 44.648749)))
    >>> f4 = Feature(geometry=Point((-63.573589, 44.641788)))
    >>> f5 = Feature(geometry=Point((-63.587665, 44.64533)))
    >>> f6 = Feature(geometry=Point((-63.595218, 44.64765)))
    >>> fc = [f1, f2, f3, f4, f5, f6]
    >>> concave(FeatureCollection(fc), alpha=100)
    """
    points = get_points(features)

    concave_hull, edges = _alpha_shape(points, alpha)

    return Feature(geometry=mapping(concave_hull))


def convex(features: FeatureCollection):
    """
    Generate convex hull for the given feature or Feature Collection
    :param features: It can be a feature or Feature Collection
    :return: Feature of convex hull polygon

    Example:
    >>> from turfpy.transformation import convex
    >>> from geojson import FeatureCollection, Feature, Point
    >>> f1 = Feature(geometry=Point((10.195312, 43.755225)))
    >>> f2 = Feature(geometry=Point((10.404052, 43.8424511)))
    >>> f3 = Feature(geometry=Point((10.579833, 43.659924)))
    >>> f4 = Feature(geometry=Point((10.360107, 43.516688)))
    >>> f5 = Feature(geometry=Point((10.14038, 43.588348)))
    >>> f6 = Feature(geometry=Point((10.195312, 43.755225)))
    >>> fc = [f1, f2, f3, f4, f5, f6]
    >>> convex(FeatureCollection(fc))
    """
    points = get_points(features)

    point_collection = geometry.MultiPoint(list(points))

    return Feature(geometry=mapping(point_collection.convex_hull))

"""
This module implements some of the spatial analysis techniques and processes used to
understand the patterns and relationships of geographic features.
This is mainly inspired by turf.js.
link: http://turfjs.org/
"""
import copy
import itertools
import math
from math import floor, sqrt
from typing import List, Optional, Union

import numpy as np
from geojson import Feature, FeatureCollection, LineString, MultiLineString
from geojson import Point as GeoPoint
from geojson import Polygon
from scipy.spatial import Delaunay, Voronoi
from shapely import geometry as geometry
from shapely.geometry import LineString as ShapelyLineString
from shapely.geometry import MultiPoint, MultiPolygon, Point, mapping, shape
from shapely.ops import cascaded_union, clip_by_rect, polygonize, unary_union

from turfpy.helper import get_coord, get_coords, get_geom, get_type, length_to_degrees
from turfpy.measurement import (
    bbox,
    bbox_polygon,
    center,
    centroid,
    destination,
    rhumb_bearing,
    rhumb_destination,
    rhumb_distance,
)
from turfpy.meta import coord_each, feature_each, flatten_each

from .dev_lib.earcut import earcut
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


def bbox_clip(geojson: Feature, bbox: list) -> Feature:
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


def intersect(features: Union[List[Feature], FeatureCollection]) -> Feature:
    """
    Takes polygons and finds their intersection
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
    properties_list = []

    if isinstance(features, list):
        shapes = []
        for f in features:
            poly = get_geom(f)
            s = shape(poly)
            shapes.append(s)

            if "properties" in f.keys():
                properties_list.append(f["properties"])

    else:
        if "features" not in features.keys():
            raise Exception("Invalid FeatureCollection")

        if "properties" in features.keys():
            properties_list.append(features["properties"])

        shapes = []
        for f in features["features"]:
            poly = get_geom(f)
            s = shape(poly)
            shapes.append(s)

            if "properties" in f.keys():
                properties_list.append(f["properties"])

    intersection = shapes[0]

    for shape_value in shapes:
        intersection = shape_value.intersection(intersection)

    intersection = mapping(intersection)

    if len(intersection["coordinates"]) == 0:
        return None

    properties = merge_dict(properties_list)

    intersection_feature = Feature(geometry=intersection, properties=properties)

    return intersection_feature


def bezie_spline(line: Feature, resolution=10000, sharpness=0.85) -> Feature:
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


def merge_dict(dicts: list):
    super_dict: dict = {}
    for d in dicts:
        for k, v in d.items():
            if k not in super_dict.keys():
                super_dict[k] = v
            else:
                if isinstance(super_dict[k], list):
                    if v not in super_dict[k]:
                        super_dict[k].append(v)
                else:
                    if super_dict[k] != v:
                        super_dict[k] = [super_dict[k], v]
    return super_dict


def union(
    features: Union[List[Feature], FeatureCollection]
) -> Union[Feature, FeatureCollection]:
    """
    Given list of features or ``FeatureCollection`` return union of those.

    :param features: A list of GeoJSON features or FeatureCollection.
    :return: A GeoJSON Feature or FeatureCollection.

    Example:
        >>> from turfpy.transformation import union
        >>> from geojson import Feature, Polygon, FeatureCollection
        >>> f1 = Feature(geometry=Polygon([[
        ...          [-82.574787, 35.594087],
        ...          [-82.574787, 35.615581],
        ...          [-82.545261, 35.615581],
        ...          [-82.545261, 35.594087],
        ...          [-82.574787, 35.594087]
        ...      ]]), properties={"fill": "#00f"})
        >>> f2 = Feature(geometry=Polygon([[
        ...          [-82.560024, 35.585153],
        ...          [-82.560024, 35.602602],
        ...          [-82.52964, 35.602602],
        ...          [-82.52964, 35.585153],
        ...          [-82.560024, 35.585153]]]), properties={"fill": "#00f"})
        >>> union(FeatureCollection([f1, f2], properties={"combine": "yes"}))
    """

    shapes = []
    properties_list = []
    if isinstance(features, list):
        for f in features:
            if f.type != "Feature":
                raise Exception("Not a valid feature")
            geom = get_geom(f)
            s = shape(geom)
            shapes.append(s)

            if "properties" in f.keys():
                properties_list.append(f["properties"])
    else:
        if "features" not in features.keys():
            raise Exception("Invalid FeatureCollection")
        if "properties" in features.keys():
            properties_list.append(features["properties"])

        for f in features["features"]:
            geom = get_geom(f)
            s = shape(geom)
            shapes.append(s)

            if "properties" in f.keys():
                properties_list.append(f["properties"])

    result = cascaded_union(shapes)
    result = mapping(result)
    properties = merge_dict(properties_list)

    if result["type"] == "GeometryCollection":
        features = []
        for geom in result["geometries"]:
            features.append(Feature(geometry=geom))
        return FeatureCollection(features, properties=properties)

    return Feature(geometry=result, properties=properties)


def _alpha_shape(points, alpha):
    """
    Compute the alpha shape (concave hull) of a set of points.

    :param points: Iterable container of points.
    :param alpha: alpha value to influence the gooeyness of the border. Smaller
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


def concave(features: Union[Feature, FeatureCollection], alpha=2):
    """Generate concave hull for the given feature or Feature Collection.

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


def convex(features: Union[Feature, FeatureCollection]):
    """Generate convex hull for the given feature or Feature Collection

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


def dissolve(
    features: Union[List[Feature], FeatureCollection], property_name: str = None
) -> FeatureCollection:
    """
    Take FeatureCollection or list of features to dissolve based on
    property_name provided.
    :param features: A list of GeoJSON features or FeatureCollection.
    :param property_name: Name of property based on which to dissolve.
    :return: A GeoJSON Feature or FeatureCollection.

    Example:

    >>> from geojson import Polygon, Feature, FeatureCollection
    >>> from turfpy.transformation import dissolve
    >>> f1 = Feature(geometry=Polygon([[
    >>>     [0, 0],
    >>>     [0, 1],
    >>>     [1, 1],
    >>>     [1, 0],
    >>>     [0, 0]]]), properties={"combine": "yes", "fill": "#00f"})
    >>> f2 = Feature(geometry=Polygon([[
    >>>     [0, -1],
    >>>     [0, 0],
    >>>     [1, 0],
    >>>     [1, -1],
    >>>     [0,-1]]]), properties={"combine": "yes"})
    >>> f3 = Feature(geometry=Polygon([[
    >>>     [1,-1],
    >>>     [1, 0],
    >>>     [2, 0],
    >>>     [2, -1],
    >>>     [1, -1]]]), properties={"combine": "no"})
    >>> dissolve(FeatureCollection([f1, f2, f3]), property_name='combine')
    """
    if isinstance(features, list):
        features = FeatureCollection(features)

    if "features" not in features.keys():
        raise Exception("Invalid FeatureCollection")
    dissolve_feature_list = []
    if property_name:
        for k, g in itertools.groupby(
            features["features"], key=lambda x: x["properties"].get(property_name)
        ):
            fc = FeatureCollection(list(g))
            # if "properties" in features.keys():
            #     fc['properties'] = features['properties']
            result = union(fc)
            if result["type"] == "FeatureCollection":
                for f in result["features"]:
                    dissolve_feature_list.append(f)
            else:
                dissolve_feature_list.append(result)
    else:
        return union(features)
    if "properties" in features.keys():
        return FeatureCollection(dissolve_feature_list, properties=features["properties"])
    else:
        return FeatureCollection(dissolve_feature_list)


def difference(feature_1: Feature, feature_2: Feature) -> Feature:
    """
    Find the difference between given two features.
    :param feature_1: A GeoJSON feature
    :param feature_2: A GeoJSON feature
    :return: A GeoJSON feature

    Example:

    >>> from geojson import Polygon, Feature
    >>> from turfpy.transformation import difference
    >>> f1 = Feature(geometry=Polygon([[
    >>>     [128, -26],
    >>>     [141, -26],
    >>>     [141, -21],
    >>>     [128, -21],
    >>>     [128, -26]]]), properties={"combine": "yes", "fill": "#00f"})
    >>> f2 = Feature(geometry=Polygon([[
    >>>     [126, -28],
    >>>     [140, -28],
    >>>     [140, -20],
    >>>     [126, -20],
    >>>     [126, -28]]]), properties={"combine": "yes"})
    >>> difference(f1, f2)
    """
    properties_list = []

    if "properties" in feature_1.keys():
        properties_list.append(feature_1["properties"])

    if "properties" in feature_2.keys():
        properties_list.append(feature_2["properties"])

    shape_1 = shape(get_geom(feature_1))

    shape_2 = shape(get_geom(feature_2))

    difference_result = shape_1.difference(shape_2)

    difference_result = mapping(difference_result)

    if len(difference_result["coordinates"]) == 0:
        return None

    properties = merge_dict(properties_list)

    difference_feature = Feature(geometry=difference_result, properties=properties)

    return difference_feature


def transform_rotate(
    feature: Union[List[Feature], FeatureCollection],
    angle: float,
    pivot: list = None,
    mutate: bool = False,
):
    """
    Rotates any geojson Feature or Geometry of a specified angle,
    around its centroid or a given pivot
    point; all rotations follow the right-hand rule.

    :param feature: Geojson to be rotated.
    :param angle: angle of rotation (along the vertical axis),
        from North in decimal degrees, negative clockwise
    :param pivot: point around which the rotation will be performed
    :param mutate: allows GeoJSON input to be mutated
        (significant performance increase if True)
    :return: the rotated GeoJSON

    Example :-

    >>> from turfpy.transformation import transform_rotate
    >>> from geojson import Polygon, Feature
    >>> f = Feature(geometry=Polygon([[[0,29],[3.5,29],[2.5,32],[0,29]]]))
    >>> pivot = [0, 25]
    >>> transform_rotate(f, 10, pivot)
    """
    if not feature:
        raise Exception("geojson is required")

    if angle == 0:
        return feature

    if not pivot:
        pivot = centroid(feature)["geometry"]["coordinates"]

    if not mutate:
        feature = copy.deepcopy(feature)

    def _callback_coord_each(
        coord, coord_index, feature_index, multi_feature_index, geometry_index
    ):
        nonlocal pivot, angle
        initial_angle = rhumb_bearing(GeoPoint(pivot), GeoPoint(coord))
        final_angle = initial_angle + angle
        distance = rhumb_distance(GeoPoint(pivot), GeoPoint(coord))
        new_coords = get_coord(rhumb_destination(GeoPoint(pivot), distance, final_angle))
        coord[0] = new_coords[0]
        coord[1] = new_coords[1]

    coord_each(feature, _callback_coord_each)

    return feature


def transform_translate(
    feature: Union[List[Feature], FeatureCollection],
    distance: float,
    direction: float,
    units: str = "km",
    z_translation: float = 0,
    mutate: bool = False,
):
    """
    Moves any geojson Feature or Geometry
    of a specified distance along a
    Rhumb Line on the provided direction angle.

    :param feature: Geojson data that is to be translated
    :param distance: length of the motion;
        negative values determine motion in opposite direction
    :param direction: of the motion; angle
        from North in decimal degrees, positive clockwise
    :param units: units for the distance and z_translation
    :param z_translation: length of the vertical motion, same unit of distance
    :param mutate: allows GeoJSON input to be mutated
        (significant performance increase if true)
    :return: the translated GeoJSON

    Example :-

    >>> from turfpy.transformation import transform_translate
    >>> from geojson import Polygon, Feature
    >>> f = Feature(geometry=Polygon([[[0,29],[3.5,29],[2.5,32],[0,29]]]))
    >>> transform_translate(f, 100, 35, mutate=True)
    """
    if not feature:
        raise Exception("geojson is required")

    if not distance:
        raise Exception("distance is required")

    if distance == 0 and z_translation == 0:
        return feature

    if not direction:
        raise Exception("direction is required")

    if distance < 0:
        distance = -distance
        direction = direction + 180

    if not mutate:
        feature = copy.deepcopy(feature)

    def _callback_coord_each(
        coord, coord_index, feature_index, multi_feature_index, geometry_index
    ):
        nonlocal distance, direction, units, z_translation
        new_coords = get_coord(
            rhumb_destination(GeoPoint(coord), distance, direction, {units: units})
        )
        coord[0] = new_coords[0]
        coord[1] = new_coords[1]
        if z_translation and len(coord) == 3:
            coord[2] += z_translation

    coord_each(feature, _callback_coord_each)

    return feature


def transform_scale(
    features,
    factor: float,
    origin: Union[str, list] = "centroid",
    mutate: bool = False,
):
    """
    Scale a GeoJSON from a given
    point by a factor of scaling
    (ex: factor=2 would make the GeoJSON 200% larger).
    If a FeatureCollection is provided, the origin
    point will be calculated based on each individual Feature.

    :param features: GeoJSON to be scaled
    :param factor: of scaling, positive or negative values greater than 0
    :param origin: Point from which the scaling will occur
        (string options: sw/se/nw/ne/center/centroid)
    :param mutate: allows GeoJSON input to be mutated
        (significant performance increase if true)
    :return: Scaled Geojson

    Example :-

    >>> from turfpy.transformation import transform_scale
    >>> from geojson import Polygon, Feature
    >>> f = Feature(geometry=Polygon([[[0,29],[3.5,29],[2.5,32],[0,29]]]))
    >>> transform_scale(f, 3, origin=[0, 29])
    """
    if not features:
        raise Exception("geojson is required")

    if not factor:
        raise Exception("invalid factor")

    if not mutate:
        features = copy.deepcopy(features)

    if features["type"] == "FeatureCollection":

        def _callback_feature_each(feature, feature_index):
            nonlocal factor, origin, features
            features["features"][feature_index] = scale(feature, factor, origin)

        feature_each(features, _callback_feature_each)
        return features

    return scale(features, factor, origin)


def scale(feature, factor, origin):
    is_point = get_type(feature) == "Point"
    origin = define_origin(feature, origin)

    if factor == 1 or is_point:
        return feature

    def _callback_coord_each(
        coord, coord_index, feature_index, multi_feature_index, geometry_index
    ):
        nonlocal factor, origin
        original_distance = rhumb_distance(GeoPoint(origin), GeoPoint(coord))
        bearing = rhumb_bearing(GeoPoint(origin), GeoPoint(coord))
        new_distance = original_distance * factor
        new_coord = get_coord(rhumb_destination(GeoPoint(origin), new_distance, bearing))
        coord[0] = new_coord[0]
        coord[1] = new_coord[1]
        if len(coord) == 3:
            coord[2] = coord[2] * factor

    coord_each(feature, _callback_coord_each)

    return feature


def define_origin(geojson, origin):
    if not origin:
        origin = "centroid"

    if isinstance(origin, list):
        return get_coord(origin)

    bb = bbox(geojson)
    west = bb[0]
    south = bb[1]
    east = bb[2]
    north = bb[3]

    if (
        origin == "sw"
        or origin == "southwest"
        or origin == "westsouth"
        or origin == "bottomleft"
    ):
        return [west, south]
    elif (
        origin == "se"
        or origin == "southeast"
        or origin == "eastsouth"
        or origin == "bottomright"
    ):
        return [east, south]
    elif (
        origin == "nw"
        or origin == "northwest"
        or origin == "westnorth"
        or origin == "topleft"
    ):
        return [west, north]
    elif (
        origin == "ne"
        or origin == "northeast"
        or origin == "eastnorth"
        or origin == "topright"
    ):
        return [east, north]
    elif origin == "center":
        return center(geojson)["geometry"]["coordinates"]
    elif origin is None or origin == "centroid":
        return centroid(geojson)["geometry"]["coordinates"]
    else:
        raise Exception("invalid origin")


def tesselate(poly: Feature) -> FeatureCollection:
    """Tesselates a Feature into a FeatureCollection of triangles using earcut.

    :param poly: A GeoJSON feature ``class:geojson.Polygon``.
    :return: A GeoJSON FeatureCollection of triangular polygons.

    Example:
    >>> from geojson import Feature
    >>> from turfpy.transformation import tesselate
    >>> polygon = Feature(geometry={"coordinates": [[[11, 0], [22, 4], [31, 0], [31, 11],
    ... [21, 15], [11, 11], [11, 0]]], "type": "Polygon"})
    >>> tesselate(polygon)
    """
    if poly.geometry.type != "Polygon" and poly.geometry.type != "MultiPolygon":
        raise ValueError("Geometry must be Polygon or MultiPolygon")

    fc = FeatureCollection([])

    if poly.geometry.type == "Polygon":
        fc["features"] = __process_polygon(poly.geometry.coordinates)
    else:
        for co in poly.geometry.coordinates:
            fc["features"].extend(__process_polygon(co))
    return fc


def __process_polygon(coordinates):
    data = __flatten_coords(coordinates)
    dim = 2
    result = earcut(data["vertices"], data["holes"], dim)

    features = []
    vertices = []
    for i, val in enumerate(result):
        index = val
        vertices.append(
            [data["vertices"][index * dim], data["vertices"][index * dim + 1]]
        )
    i = 0
    while i < len(vertices):
        coords = vertices[i : i + 3]
        coords.append(vertices[i])
        features.append(Feature(geometry={"coordinates": [coords], "type": "Polygon"}))
        i += 3
    return features


def __flatten_coords(data):
    dim = len(data[0][0])
    result = {"vertices": [], "holes": [], "dimensions": dim}
    hole_index = 0
    for i, val in enumerate(data):
        for j, _ in enumerate(val):
            for d in range(dim):
                result["vertices"].append(data[i][j][d])
        if i > 0:
            hole_index += len(data[i - 1])
            result["holes"].append(hole_index)
    return result


def line_offset(geojson: Feature, distance: float, unit: str = "km") -> Feature:
    """
    Takes a linestring or multilinestring and returns
    a line at offset by the specified distance.

    :param geojson: input GeoJSON
    :param distance: distance to offset the line (can be of negative value)
    :param unit: Units in which distance to be calculated, values can be 'deg', 'rad',
        'mi', 'km', default is 'km'
    :return: Line feature offset from the input line

    Example:
    >>> from geojson import MultiLineString, Feature
    >>> from turfpy.transformation import line_offset
    >>> ls = Feature(geometry=MultiLineString([
    >>>      [(3.75, 9.25), (-130.95, 1.52)],
    >>>      [(23.15, -34.25), (-1.35, -4.65), (3.45, 77.95)]
    >>>  ]))
    >>> line_offset(ls, 2, unit='mi')
    """
    if not geojson:
        raise Exception("geojson is required")

    if not distance:
        raise Exception("distance is required")

    type = get_type(geojson)
    properties = geojson.get("properties", {})

    if type == "LineString":
        return line_offset_feature(geojson, distance, unit)
    elif type == "MultiLineString":
        coords = []

        def callback_flatten_each(feature, feature_index, multi_feature_index):
            nonlocal coords
            coords.append(
                line_offset_feature(feature, distance, unit).geometry.coordinates
            )
            return True

        flatten_each(geojson, callback_flatten_each)
        return Feature(geometry=MultiLineString(coords), properties=properties)


def line_offset_feature(line, distance, units):
    segments = []
    offset_degrees = length_to_degrees(distance, units)
    coords = get_coords(line)
    final_coords = []

    for index, current_coords in enumerate(coords):
        if index != len(coords) - 1:
            segment = _process_segment(current_coords, coords[index + 1], offset_degrees)
            segments.append(segment)
            if index > 0:
                seg2_coords = segments[index - 1]
                intersects = _intersection(segment, seg2_coords)

                if intersects:
                    seg2_coords[1] = intersects
                    segment[0] = intersects

                final_coords.append(seg2_coords[0])
                if index == len(coords) - 2:
                    final_coords.append(segment[0])
                    final_coords.append(segment[1])

            if len(coords) == 2:
                final_coords.append(segment[0])
                final_coords.append(segment[1])

    return Feature(
        geometry=LineString(final_coords), properties=line.get("properties", {})
    )


def _process_segment(point1, point2, offset):
    L = sqrt(
        (point1[0] - point2[0]) * (point1[0] - point2[0])
        + (point1[1] - point2[1]) * (point1[1] - point2[1])
    )

    out1x = point1[0] + offset * (point2[1] - point1[1]) / L
    out2x = point2[0] + offset * (point2[1] - point1[1]) / L
    out1y = point1[1] + offset * (point1[0] - point2[0]) / L
    out2y = point2[1] + offset * (point1[0] - point2[0]) / L
    return [[out1x, out1y], [out2x, out2y]]


def _intersection(a, b):
    if _is_parallel(a, b):
        return False
    return _intersect_segments(a, b)


def _is_parallel(a, b):
    r = _ab(a)
    s = _ab(b)
    return _cross_product(r, s) == 0


def _ab(segment):
    start = segment[0]
    end = segment[1]
    return [end[0] - start[0], end[1] - start[1]]


def _cross_product(v1, v2):
    return (v1[0] * v2[1]) - (v2[0] * v1[1])


def _intersect_segments(a, b):
    p = a[0]
    r = _ab(a)
    q = b[0]
    s = _ab(b)

    cross = _cross_product(r, s)
    qmp = _sub(q, p)
    numerator = _cross_product(qmp, s)
    t = numerator / cross
    intersection = _add(p, _scalar_mult(t, r))
    return intersection


def _add(v1, v2):
    return [v1[0] + v2[0], v1[1] + v2[1]]


def _sub(v1, v2):
    return [v1[0] - v2[0], v1[1] - v2[1]]


def _scalar_mult(s, v):
    return [s * v[0], s * v[1]]


def voronoi(
    points: Union[FeatureCollection, List], bbox: Optional[list] = None
) -> Feature:
    """Takes a FeatureCollection of points, and a bounding box,
    and returns a FeatureCollection of Voronoi polygons.

    :param points: To find the Voronoi polygons around. Points should be either
        FeatureCollection of points or list of points.
    :param bbox: A bounding box to clip.
    :return: A GeoJSON Feature.

    Example:
    >>> from turfpy.transformation import voronoi

    >>> points = [
    ... [-66.9703, 40.3183],
    ... [-63.7763, 40.4500],
    ... [-65.4196, 42.13985310302137],
    ... [-69.5813, 43.95405461286195],
    ... [-65.66337553550034, 55.97088945355232],
    ... [-60.280418548905, 56.240669185466146],
    ... [-68.5129561347689, 50.12984589640148],
    ... [-64.2393519226657, 59.66235385923687],
    ... ]
    >>> bbox = [-70, 40, -60, 60]
    >>> voronoi(points, bbox)
    """
    if isinstance(points, FeatureCollection):
        coords = []
        for feature in points["features"]:
            coords.append(feature["features"][0]["geometry"]["coordinates"])
        points = np.array(coords)
    elif isinstance(points, list):
        points = np.array(points)
    else:
        raise ValueError(
            "points should be either FeatureCollection of points of List of Points"
        )
    vor = Voronoi(points)
    lines = [
        ShapelyLineString(vor.vertices[line])
        for line in vor.ridge_vertices
        if -1 not in line
    ]

    convex_hull = MultiPoint([Point(i) for i in points]).convex_hull.buffer(2)
    result = MultiPolygon([poly.intersection(convex_hull) for poly in polygonize(lines)])
    result = MultiPolygon(
        [p for p in result] + [p for p in convex_hull.difference(unary_union(result))]
    )
    if bbox is not None:
        w, s, e, n = bbox
        cliped_result = clip_by_rect(result, w, s, e, n)
        return Feature(geometry=cliped_result)
    return Feature(geometry=result)

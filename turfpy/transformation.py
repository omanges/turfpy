"""
This module implements some of the spatial analysis techniques and processes used to
understand the patterns and relationships of geographic features.
This is mainly inspired by turf.js.
link: http://turfjs.org/
"""
from geojson import Feature, Polygon

from turfpy.helper import get_geom
from turfpy.measurement import destination, bbox_polygon

from shapely.geometry import shape, mapping


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
        bearing = i * -360 / radius
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
    >>> from turfpy.transformation import bbox_clip
    >>> from geojson import Feature
    >>> f = Feature(geometry={"coordinates": [[[2, 2], [8, 4],
    >>> [12, 8], [3, 7], [2, 2]]], "type": "Polygon"})
    >>> bbox = [0, 0, 10, 10]
    >>> clip = bbox_clip(f, bbox)
    """
    bb_polygon = bbox_polygon(bbox)

    bb_clip = intersect(geojson, bb_polygon)

    if "properties" in geojson:
        bb_clip.properties = geojson["properties"]

    return bb_clip


def intersect(geojson_1: Feature, geojson_2: Feature):
    """
    Takes two polygons and finds their intersection
    :param geojson_1: Geojson data
    :param geojson_2: Geojson data
    :return: Intersection Geojson Feature
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
    >>> inter = intersect(f, b)
    """

    geometry_1 = get_geom(geojson_1)
    geometry_2 = get_geom(geojson_2)

    shape_1 = shape(geometry_1)
    shape_2 = shape(geometry_2)

    intersection = shape_1.intersection(shape_2)
    intersection = mapping(intersection)

    intersection_feature = Feature(geometry=intersection)

    return intersection_feature

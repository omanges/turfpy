"""
This module implements some of the methods that allows to
generate some random spatial data.
This is mainly inspired by turf.js.
link: http://turfjs.org/
"""

import random
from typing import Any, Optional

from geojson import Feature, FeatureCollection, Point


def random_position(bbox: Optional[list[Any]] = None):
    """
    Generates a random position, if bbox provided then the
    generated position will be in the bbox.

    :param bbox: Bounding box extent in west, south, east, north order
    :return: A position as coordinates.

    Exmample:

    >>> from turfpy.random import random_position
    >>> random_position(bbox=[11.953125,
    >>> 18.979025953255267, 52.03125, 46.558860303117164])
    """
    if not bbox:
        return [lon(), lat()]

    if len(bbox) != 4:
        raise Exception("bbox with 4 positions are only supported")

    return coord_in_bbox(bbox)


def rnd():
    return random.random() - 0.5


def lon():
    return rnd() * 360


def lat():
    return rnd() * 180


def coord_in_bbox(bbox: list):
    return [
        random.random() * (bbox[2] - bbox[0]) + bbox[0],
        random.random() * (bbox[3] - bbox[1]) + bbox[1],
    ]


def random_points(count: int = 1, bbox: Optional[list[Any]] = None) -> FeatureCollection:
    """
    Generates geojson random points, if bbox provided then the
    generated points will be in the bbox.

    :param count: Number of points to be generated, default value is one.
    :param bbox: Bounding box extent in west, south, east, north order
    :return: A FeatureCollection of generated points.

    Exmample:

    >>> from turfpy.random import random_points
    >>> random_points(count=3, bbox=[11.953125,
    >>> 18.979025953255267, 52.03125, 46.558860303117164])
    """
    features = []
    for i in range(count):
        features.append(Feature(geometry=Point(random_position(bbox))))

    return FeatureCollection(features)

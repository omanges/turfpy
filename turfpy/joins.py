"""
This module implements some of the spatial analysis techniques and processes used to
understand the patterns and relationships of geographic features.
This is mainly inspired by turf.js.
link: http://turfjs.org/
"""

import concurrent.futures
from functools import partial
from multiprocessing import Manager
from multiprocessing.managers import ListProxy
from typing import Union

from geojson import Feature, FeatureCollection, Point, Polygon

from turfpy.boolean import boolean_point_in_polygon
from turfpy.meta import geom_each


def points_within_polygon(
    points: Union[Feature, FeatureCollection],
    polygons: Union[Feature, FeatureCollection],
    chunk_size: int = 1,
) -> FeatureCollection:
    """Find Point(s) that fall within (Multi)Polygon(s).

    This function takes two inputs GeoJSON Feature :class:`geojson.Point` or
    :class:`geojson.FeatureCollection` of Points and GeoJSON Feature
    :class:`geojson.Polygon` or Feature :class:`geojson.MultiPolygon` or
    FeatureCollection of :class:`geojson.Polygon` or Feature
    :class:`geojson.MultiPolygon`. and returns all points with in in those
    Polygon(s) or (Multi)Polygon(s).

    :param points: A single GeoJSON ``Point`` feature or FeatureCollection of Points.
    :param polygons: A Single GeoJSON Polygon/MultiPolygon or FeatureCollection of
        Polygons/MultiPolygons.
    :param chunk_size: Number of chunks each process to handle. The default value is
            1, for a large number of features please use `chunk_size` greater than 1
            to get better results in terms of performance.
    :return: A :class:`geojson.FeatureCollection` of Points.
    """
    if not points:
        raise Exception("Points cannot be empty")

    if points["type"] == "Point":
        points = FeatureCollection([Feature(geometry=points)])

    if points["type"] == "Feature":
        points = FeatureCollection([points])

    manager = Manager()
    results: ListProxy[dict] = manager.list()

    part_func = partial(
        check_each_point,
        polygons=polygons,
        results=results,
    )

    with concurrent.futures.ProcessPoolExecutor() as executor:
        for _ in executor.map(part_func, points["features"], chunksize=chunk_size):
            pass

    return FeatureCollection(list(results))


def check_each_point(point: Point, polygons: list[Polygon], results: ListProxy):
    """
    Check each point with in the polygon(s) and append the point to the results list

    :param point: A single GeoJSON Point feature.
    :type point: dict
    :param polygons: A list of GeoJSON Polygon/MultiPolygon.
    :type polygons: list
    :param results: A list of GeoJSON Point features.
    :type results: list
    """

    def __callback_geom_each(
        current_geometry, feature_index, feature_properties, feature_bbox, feature_id
    ):
        contained = False
        if boolean_point_in_polygon(
            Feature(geometry=point["geometry"]), Feature(geometry=current_geometry)
        ):
            contained = True

        if contained:
            nonlocal results
            if point not in results:
                results.append(point)

    geom_each(polygons, __callback_geom_each)

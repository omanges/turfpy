from functools import reduce
from typing import List, Union

from geojson import (
    Feature,
    FeatureCollection,
    LineString,
    MultiLineString,
    MultiPolygon,
    Polygon,
)
from shapely.geometry import mapping, shape

import turfpy._compact as compat
from turfpy.helper import get_coords
from turfpy.meta import flatten_each
from turfpy.transformation import intersect


def line_intersect(
    feature1: Union[LineString, Polygon, MultiLineString, MultiPolygon, Feature],
    feature2: Union[LineString, Polygon, MultiLineString, MultiPolygon, Feature],
) -> FeatureCollection:
    """
    Takes any LineString or Polygon GeoJSON and returns the intersecting point(s).
    If one of the Features is polygon pass the polygon feature as the first
    parameter to improve performance. To use this functionality Rtree or pygeos
    is needed to be installed.

    See installation instructions at https://geopandas.org/install.html

    :param feature1: Any LineString or Polygon, if one of the two features is
        polygon to improve performance please pass polygon as this parameter.
    :param feature2: Any LineString or Polygon.
    :return: FeatureCollection of intersecting points.

    Exmaple:
    >>> from geojson import LineString, Feature
    >>> from turfpy.misc import line_intersect
    >>> l1 = Feature(geometry=LineString([[126, -11], [129, -21]]))
    >>> l2 = Feature(geometry=LineString([[123, -18], [131, -14]]))
    >>> line_intersect(l1, l2)
    """
    if not compat.HAS_GEOPANDAS or not compat.HAS_PYGEOS:
        raise ImportError(
            "line_intersect requires `Spatial indexes` for which it "
            "requires `geopandas` and either `rtree` or `pygeos`. "
            "See installation instructions at https://geopandas.org/install.html"
        )
    import geopandas  # noqa

    unique = set()
    results: List[Feature] = []
    f1 = feature1
    f2 = feature2
    if f1["type"] != "Feature":
        f1 = Feature(geometry=f1)

    if f2["type"] != "Feature":
        f2 = Feature(geometry=f2)

    if (
        f1["geometry"]
        and f2["geometry"]
        and f1["geometry"]["type"] == "LineString"
        and f2["geometry"]["type"] == "LineString"
        and len(f1["geometry"]["coordinates"]) == 2
        and len(f2["geometry"]["coordinates"]) == 2
    ):
        inters = intersect([f1, f2])
        if inters:
            results.append(inters)
        return FeatureCollection(results)

    segments = line_segment(f1)
    gdf = geopandas.GeoDataFrame.from_features(segments)
    spatial_index = gdf.sindex
    segments = line_segment(f2)["features"]

    for segment in segments:
        s = shape(segment["geometry"])
        possible_matches_index = list(spatial_index.intersection(s.bounds))
        possible_matches = gdf.iloc[possible_matches_index]
        precise_matches = possible_matches[possible_matches.intersects(s)]
        if not precise_matches.empty:
            for index, row in precise_matches.iterrows():
                # intersect = intersects(mapping(row["geometry"]), segment)
                intersection = Feature(geometry=mapping(row["geometry"].intersection(s)))
                key = ",".join(map(str, get_coords(intersection)))
                if key not in unique:
                    unique.add(key)
                    results.append(intersection)

    return FeatureCollection(results)


def line_segment(
    geojson: Union[LineString, Polygon, MultiLineString, MultiPolygon, Feature]
) -> FeatureCollection:
    """
    Creates a FeatureCollection of 2-vertex LineString segments from a
    (Multi)LineString or (Multi)Polygon.
    :param geojson: GeoJSON Polygon or LineString
    :return: FeatureCollection of 2-vertex line segments

    Example:
    >>> from turfpy.misc import line_segment
    >>>
    >>> poly = {
    >>>       "type": "Feature",
    >>>       "properties": {},
    >>>       "geometry": {
    >>>         "type": "Polygon",
    >>>         "coordinates": [
    >>>           [
    >>>             [
    >>>               51.17431640625,
    >>>               47.025206001585396
    >>>             ],
    >>>             [
    >>>               45.17578125,
    >>>               43.13306116240612
    >>>             ],
    >>>             [
    >>>               54.5361328125,
    >>>               41.85319643776675
    >>>             ],
    >>>             [
    >>>               51.17431640625,
    >>>               47.025206001585396
    >>>             ]
    >>>           ]
    >>>         ]
    >>>       }
    >>> }
    >>>
    >>> line_segment(poly)
    """
    if not geojson:
        raise Exception("geojson is required!!!")

    results: List[Feature] = []

    def callback_flatten_each(feature, feature_index, multi_feature_index):
        line_segment_feature(feature, results)

    flatten_each(geojson, callback_flatten_each)

    return FeatureCollection(results)


def line_segment_feature(geojson: Union[LineString, Polygon], results: List[Feature]):
    coords = []
    geometry = geojson["geometry"]

    if geometry:
        if geometry["type"] == "Polygon":
            coords = get_coords(geometry)
        elif geometry["type"] == "LineString":
            coords = [get_coords(geometry)]

        for coord in coords:
            segments = create_segments(coord, geojson["properties"])

            for segment in segments:
                segment["id"] = len(results)
                results.append(segment)


def create_segments(coords, properties):
    segments = []

    def callback(current_coords, previous_coords):
        segment = Feature(
            geometry=LineString([previous_coords, current_coords]), properties=properties
        )
        segment.bbox = bbox(previous_coords, current_coords)
        segments.append(segment)
        return previous_coords

    reduce(callback, coords)

    return segments


def bbox(coords1, coords2):
    x1 = coords1[0]
    y1 = coords1[1]
    x2 = coords2[0]
    y2 = coords2[1]
    if x1 < x2:
        west = x1
    else:
        west = x2

    if y1 < y2:
        south = y1
    else:
        south = y2

    if x1 > x2:
        east = x1
    else:
        east = x2

    if y1 > y2:
        north = y1
    else:
        north = y2

    return [west, south, east, north]

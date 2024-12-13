"""
This module implements some of the spatial analysis techniques and processes used to
analyse geojson linestring. This is mainly inspired by turf.js Misc section.
link: http://turfjs.org/
"""

from functools import reduce
from typing import List, Union

import geopandas
from geojson import (
    Feature,
    FeatureCollection,
    LineString,
    MultiLineString,
    MultiPolygon,
    Point,
    Polygon,
)
from shapely.geometry import mapping, shape

from turfpy.helper import convert_angle_to_360, get_coord, get_coords, get_type
from turfpy.measurement import bearing, destination, distance
from turfpy.meta import coord_each, flatten_each
from turfpy.transformation import circle, intersect


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
    geojson: Union[LineString, Polygon, MultiLineString, MultiPolygon, Feature],
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
    ...       "type": "Feature",
    ...       "properties": {},
    ...       "geometry": {
    ...         "type": "Polygon",
    ...         "coordinates": [
    ...           [
    ...             [
    ...               51.17431640625,
    ...               47.025206001585396
    ...             ],
    ...             [
    ...               45.17578125,
    ...               43.13306116240612
    ...             ],
    ...             [
    ...               54.5361328125,
    ...               41.85319643776675
    ...             ],
    ...             [
    ...               51.17431640625,
    ...               47.025206001585396
    ...             ]
    ...           ]
    ...         ]
    ...       }
    ... }
    ...
    >>> line_segment(poly)
    """
    if not geojson:
        raise Exception("geojson is required!!!")

    results: List[Feature] = []

    def callback_flatten_each(feature, feature_index, multi_feature_index):
        line_segment_feature(feature, results)
        return True

    flatten_each(geojson, callback_flatten_each)

    return FeatureCollection(results)


def line_segment_feature(geojson: Union[LineString, Polygon], results: List[Feature]):
    """

    :param geojson:
    :param results:
    :return:
    """
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
    """
    Create Segments from LineString coordinates
    :param coords: coords LineString coordinates
    :param properties: properties GeoJSON properties
    :return: Line segments Features
    """
    segments = []

    def callback(current_coords, previous_coords):
        segment = Feature(
            geometry=LineString([previous_coords, current_coords]),
            properties=properties,
        )
        segment.bbox = bbox(previous_coords, current_coords)
        segments.append(segment)
        return previous_coords

    reduce(callback, coords)

    return segments


def bbox(coords1, coords2):
    """
    Create BBox between two coordinates
    :param coords1: coords1 Point coordinate
    :param coords2: coords2 Point coordinate
    :return: Bounding Box as [west, south, east, north]
    """
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


def nearest_point_on_line(
    line: Union[LineString, MultiLineString], point: Point, options: dict = {}
) -> Point:
    """
    Takes a Point and a LineString and calculates the closest Point on the
    (Multi)LineString.

    :param line: line(s) to snap to
    :param point: point to snap from
    :param options: Option like units of distance and properties to be passed to
        destination point feature. Value for units are 'mi', 'km', 'deg' and 'rad'.
    :return: Feature: closest point on the `line` to `point`. The properties object
        will contain three values:
        `index`: closest point was found on nth line part,
        `dist`: distance between pt and the closest point,
        `location`: distance along the line between start and the closest point.
    """
    closest_pt = Point([float("inf"), float("inf")], properties={"dist": float("inf")})
    length = 0.0

    def dist(pt1, pt2, options):
        if "units" in options:
            return distance(pt1, pt2, options["units"])
        else:
            return distance(pt1, pt2)

    def callback_flatten_each(feature, feature_index, multi_feature_index):
        nonlocal length
        nonlocal closest_pt

        coords = get_coords(feature)
        for i, coord in enumerate(coords[:-1]):
            # start
            start = Feature(geometry=Point(coord))
            start.properties = {"dist": dist(point, start, options)}
            # stop
            stop = Feature(geometry=Point(coords[i + 1]))
            stop.properties = {"dist": dist(point, stop, options)}
            # section length
            section_length = dist(start, stop, options)
            # perpendicular
            height_distance = max(start.properties["dist"], stop.properties["dist"])
            direction = bearing(start, stop)

            perpendicular_pt1 = destination(
                Feature(geometry=point), height_distance, direction + 90, options
            )
            perpendicular_pt2 = destination(
                Feature(geometry=point), height_distance, direction - 90, options
            )
            intersect = line_intersect(
                Feature(
                    geometry=LineString(
                        [get_coord(perpendicular_pt1), get_coord(perpendicular_pt2)]
                    )
                ),
                Feature(geometry=LineString([get_coord(start), get_coord(stop)])),
            )
            intersect_pt = None
            if len(intersect["features"]) > 0:
                intersect_pt = intersect["features"][0]
                intersect_pt.properties["dist"] = dist(point, intersect_pt, options)
                intersect_pt.properties["location"] = length + dist(
                    start, intersect_pt, options
                )

            if start.properties["dist"] < closest_pt.properties["dist"]:
                closest_pt = start
                closest_pt.properties["index"] = i
                closest_pt.properties["location"] = length

            if stop.properties["dist"] < closest_pt.properties["dist"]:
                closest_pt = stop
                closest_pt.properties["index"] = i + 1
                closest_pt.properties["location"] = length + section_length

            if (
                intersect_pt
                and intersect_pt.properties["dist"] < closest_pt.properties["dist"]
            ):
                closest_pt = intersect_pt
                closest_pt.properties["index"] = i

            # update length
            length += section_length
        # process all Features
        return True

    flatten_each(line, callback_flatten_each)

    # append preoperties from options parameter to the result
    properties = options["properties"] if "properties" in options else {}
    properties.update(closest_pt.properties)
    closest_pt.properties = dict(properties)
    return closest_pt


def line_slice(
    start_pt: Point,
    stop_pt: Point,
    line: LineString,
) -> LineString:
    """
    Takes a LineString, a start Point, and a stop Point
    and returns a subsection of the line in-between those points.
    The start & stop points don't need to fall exactly on the line.

    This can be useful for extracting only the part of a route between waypoints.

    :param start_pt: starting point
    :param stop_pt: stopping point
    :param line: line to slice
    :return: sliced line as LineString Feature
    """

    if not line or get_type(line) != "LineString":
        raise Exception("line must be a LineString")

    coords = get_coords(line)
    start_vertex = nearest_point_on_line(line, start_pt)
    stop_vertex = nearest_point_on_line(line, stop_pt)

    if start_vertex["properties"]["index"] <= stop_vertex["properties"]["index"]:
        ends = [start_vertex, stop_vertex]
    else:
        ends = [stop_vertex, start_vertex]

    clip_coords = [get_coord(ends[0])]
    clip_coords.extend(
        coords[ends[0]["properties"]["index"] + 1 : ends[1]["properties"]["index"] + 1]
    )
    clip_coords.append(get_coord(ends[1]))

    return Feature(geometry=LineString(clip_coords), properties=line["properties"].copy())


def line_arc(
    center: Feature, radius: int, bearing1: int, bearing2: int, options: dict = {}
) -> Feature:
    """
    Creates a circular arc, of a circle of the given radius and center point,
    between bearing1 and bearing2; 0 bearing is
    North of center point, positive clockwise.

    :param center: A `Point` object representing center point of circle.
    :param radius: An int representing radius of the circle.
    :param bearing1: Angle, in decimal degrees, of the first radius of the arc.
    :param bearing2: Angle, in decimal degrees, of the second radius of the arc.
    :param options: A dict representing additional properties,which can be `steps`
        which has default values as 64 and `units` which has default values of `km`
    :return: A Line String feature object.

    Example:


    >>> from turfpy.misc import line_arc
    >>> from geojson import Feature, Point
    >>> center = Feature(geometry=Point((-75, 40)))
    >>> radius = 5
    >>> bearing1 = 25
    >>> bearing2 = 47
    >>> feature = line_arc(center=center, radius=radius,
    >>>        bearing1=bearing1, bearing2=bearing2)
    """
    if not options:
        options = {}
    steps = int(options["steps"]) if options.get("steps") else 64
    units = str(options.get("units")) if options.get("units") else "km"

    angle1 = convert_angle_to_360(bearing1)
    angle2 = convert_angle_to_360(bearing2)
    properties = {}
    if center.get("type"):
        if center.get("type") == "Feature":
            properties = center.get("properties")
        else:
            raise Exception("Invalid Feature value for center parameter")

    if angle1 == angle2:
        return Feature(
            geometry=LineString(
                circle(center, radius, steps, units)["geometry"]["coordinates"][0]
            ),
            properties=properties,
        )

    arc_start_degree = angle1
    arc_end_degree = angle2 if angle1 < angle2 else angle2 + 360

    alfa = arc_start_degree
    coordinates = []
    i = 0

    while alfa < arc_end_degree:
        coordinates.append(
            destination(center, radius, alfa, {"steps": steps, "units": units})[
                "geometry"
            ]["coordinates"]
        )
        i += 1
        alfa = arc_start_degree + i * 360 / steps

    if alfa > arc_end_degree:
        coordinates.append(
            destination(center, radius, arc_end_degree, {"steps": steps, "units": units})[
                "geometry"
            ]["coordinates"]
        )

    return Feature(geometry=LineString(coordinates, properties=properties))


def sector(
    center: Feature, radius: int, bearing1: int, bearing2: int, options: dict = {}
) -> Feature:
    """
    Creates a circular sector of a circle of given radius and center Point ,
    between (clockwise) bearing1 and bearing2; 0
    bearing is North of center point, positive clockwise.

    :param center: A `Point` object representing center point of circle.
    :param radius: An int representing radius of the circle.
    :param bearing1: Angle, in decimal degrees, of the first radius of the arc.
    :param bearing2: Angle, in decimal degrees, of the second radius of the arc.
    :param options: A dict representing additional properties, which can be `steps`
        which has default values as 64, `units` which has default values of `km`,
        and `properties` which will be added to resulting Feature as properties.
    :return: A polygon feature object.

    Example:


    >>> from turfpy.misc import sector
    >>> from geojson import Feature, Point
    >>> center = Feature(geometry=Point((-75, 40)))
    >>> radius = 5
    >>> bearing1 = 25
    >>> bearing2 = 45
    >>> sector(center, radius, bearing1, bearing2)
    """
    if not options:
        options = {}
    steps = int(options["steps"]) if options.get("steps") else 64
    units = str(options.get("units")) if options.get("units") else "km"

    properties = options.get("properties") if options.get("properties") else {}

    if not center:
        raise Exception("center if required")

    if center.get("type") != "Feature":
        raise Exception("Invalid Feature value for center parameter")

    if not radius:
        raise Exception("Radius is required")

    if not bearing1:
        raise Exception("bearing1 is required")

    if not bearing2:
        raise Exception("bearing2 is required")

    if convert_angle_to_360(bearing1) == convert_angle_to_360(bearing2):
        return circle(center, radius, steps, units)

    coords = get_coords(center)

    arc = line_arc(center, radius, bearing1, bearing2, options)

    sliceCoords = [[coords]]

    def _callback_coord_each(
        coord,
        coord_index,
        feature_index,
        multi_feature_index,
        geometry_index,
    ):
        nonlocal sliceCoords
        sliceCoords[0].append(coord)

    coord_each(arc, _callback_coord_each)

    sliceCoords[0].append(coords)

    return Feature(geometry=Polygon(sliceCoords), properties=properties)

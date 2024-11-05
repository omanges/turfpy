from geojson import (
    Feature,
    FeatureCollection,
    LineString,
    MultiLineString,
    MultiPolygon,
    Polygon,
)

from turfpy.helper import get_geom


def __coords_to_line(coords, properties) -> Feature:
    """
    Convert a list of coordinates to a line

    :param coords: input coordinates
    :param properties: properties
    :return: A GeoJSON Feature
    """
    if len(coords) > 1:
        return Feature(geometry=MultiLineString(coords), properties=properties)
    return Feature(geometry=LineString(coords[0]), properties=properties)


def __single_polygon_to_line(polygon: Polygon, options=None) -> Feature:
    """
    Convert a single polygon to a line

    :param polygon: input polygon
    :param options: options
    :return: A GeoJSON Feature
    """
    if options is None:
        options = {}
    geom = get_geom(polygon)
    coords = geom["coordinates"]
    properties = options.get("properties", polygon.get("properties", {}))
    return __coords_to_line(coords, properties)


def __multi_polygon_to_line(
    multi_polygon: MultiPolygon, options=None
) -> FeatureCollection:
    """
    Convert a multi polygon to a line

    :param multi_polygon: input multi polygon
    :param options: options
    :return: A GeoJSON FeatureCollection
    """
    if options is None:
        options = {}
    geom = get_geom(multi_polygon)
    coords = geom["coordinates"]
    properties = options.get("properties", multi_polygon.get("properties", {}))
    lines = [__coords_to_line(coord, properties) for coord in coords]
    return FeatureCollection(lines)


def polygon_to_line(
    polygon: Polygon | MultiPolygon, options=None
) -> Feature | FeatureCollection:
    """
    Convert a polygon to line

    :param polygon: input polygon
    :param options: options
    :return: A GeoJSON Feature or FeatureCollection
    """

    if options is None:
        options = {}
    geom = get_geom(polygon)
    if not options.get("properties") and polygon["type"] == "Feature":
        options["properties"] = polygon.get("properties", {})

    if geom["type"] == "Polygon":
        return __single_polygon_to_line(polygon, options)
    elif geom["type"] == "MultiPolygon":
        return __multi_polygon_to_line(polygon, options)
    else:
        raise ValueError("invalid polygon")

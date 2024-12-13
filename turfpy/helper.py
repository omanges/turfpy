"""
This module will have common utilities.
"""

import math

from geojson import Feature, Point
from geojson.geometry import Geometry

avg_earth_radius_km = 6371008.8
conversions = {
    "km": 0.001,
    "m": 1.0,
    "mi": 0.000621371192,
    "ft": 3.28084,
    "in": 39.370,
    "deg": 1 / 111325,
    "cen": 100,
    "rad": 1 / avg_earth_radius_km,
    "naut": 0.000539956803,
    "yd": 0.914411119,
}


def convert_length(length, original_unit: str = "km", final_unit: str = "km"):
    """#TODO: Add description"""
    if length < 0:
        raise Exception("length must be a positive number")
    return radians_to_length(length_to_radians(length, original_unit), final_unit)


def length_to_radians(distance, unit: str = "km"):
    """#TODO: Add description"""
    if unit not in conversions:
        raise Exception(f"{unit} unit is invalid")
    b = distance / (conversions[unit] * avg_earth_radius_km)
    return b


def radians_to_length(radians, unit: str = "km"):
    """#TODO: Add description"""
    if unit not in conversions:
        raise Exception(f"{unit} unit is invalid")
    b = radians * conversions[unit] * avg_earth_radius_km
    return b


def get_type(geojson):
    """#TODO: Add description"""
    if geojson["type"] == "FeatureCollection":
        return "FeatureCollection"
    if geojson["type"] == "GeometryCollection":
        return "GeometryCollection"
    if geojson["type"] == "Feature" and "geometry" in geojson:
        return geojson["geometry"]["type"]
    return geojson["type"]


def get_coord(coord):
    """#TODO: Add description"""
    if not coord:
        raise Exception("coord is required")

    if (
        isinstance(coord, list)
        and len(coord) >= 2
        and not isinstance(coord[0], list)
        and not isinstance(coord[1], list)
    ):
        return coord
    elif (
        isinstance(coord, Feature)
        and coord["geometry"]
        and coord["geometry"]["type"] == "Point"
    ):
        return coord["geometry"]["coordinates"]
    elif isinstance(coord, Point):
        return coord["coordinates"]
    elif (
        isinstance(coord, dict)
        and coord["geometry"]
        and coord["geometry"]["type"] == "Point"
    ):
        return coord["geometry"]["coordinates"]
    else:
        raise Exception("coord must be GeoJSON Point or an Array of numbers")


def get_geom(geojson: Feature) -> Feature:
    """
    Return geometry object from a GeoJSON object.
    """
    if geojson["type"] == "Feature":
        return geojson["geometry"]
    return geojson


def get_coords(coords):
    """#TODO: Add description"""
    if isinstance(coords, list):
        return coords
    elif isinstance(coords, Feature) and coords["geometry"]:
        return coords["geometry"]["coordinates"]
    elif isinstance(coords, Geometry) and coords["coordinates"]:
        return coords["coordinates"]
    elif isinstance(coords, dict):
        return coords["coordinates"]
    else:
        raise Exception(
            "coords must be GeoJSON Feature, shapely Geometry Object, dict or an List"
        )


def feature_of(feature, ttype, name):
    """#TODO: Add description"""
    if not feature:
        raise Exception("No feature passed")

    if not name:
        raise Exception(".featureOf() requires a name")

    if not feature or feature["type"] != "Feature" or not feature["geometry"]:
        raise Exception(
            "Invalid input to " + str(name) + ", Feature with geometry required"
        )

    if not feature["geometry"] or feature["geometry"]["type"] != ttype:
        raise Exception(
            "Invalid input to "
            + name
            + ": must be a "
            + ttype
            + ", given "
            + feature["geometry"]["type"]
        )


def length_to_degrees(distance, units: str = "km"):
    """#TODO: Add description"""
    return radians_to_degrees(length_to_radians(distance, units))


def radians_to_degrees(radians: float):
    """#TODO: Add description"""
    degrees = abs(radians) % (2 * math.pi) * (1 if radians >= 0 else -1)
    return degrees * 180 / math.pi


def convert_angle_to_360(alfa: float):
    beta = alfa % 360
    if beta < 0:
        beta += 360
    return beta

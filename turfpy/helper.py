"""
This module will have common utilities.
"""

avg_earth_radius_km = 6371008.8
conversions = {'km': 0.001, 'm': 1.0, 'mi': 0.000621371192,
               'ft': 3.28084, 'in': 39.370, 'deg': 1 / 111325,
               'cen': 100, 'rad': 1 / avg_earth_radius_km, 'naut': 0.000539956803,
               'yd': 0.914411119
               }


def convert_length(length, original_unit: str = 'km', final_unit: str = 'km'):
    if length < 0:
        raise Exception('length must be a positive number')
    return radians_to_length(length_to_radians(length, original_unit), final_unit)


def length_to_radians(distance, unit: str = 'km'):
    if unit not in conversions:
        raise Exception(f'{unit} unit is invalid')
    b = distance / (conversions[unit] * avg_earth_radius_km)
    return b


def radians_to_length(radians, unit: str = 'km'):
    if unit not in conversions:
        raise Exception(f'{unit} unit is invalid')
    b = radians * conversions[unit] * avg_earth_radius_km
    return b


def get_type(geojson):
    if geojson['type'] == "FeatureCollection":
        return "FeatureCollection"
    if geojson['type'] == "GeometryCollection":
        return "GeometryCollection"
    if geojson['type'] == "Feature" and 'geometry' in geojson:
        return geojson['geometry']['type']
    return geojson['type']


def get_coord(coord):
    if not coord: raise Exception('coord is required')

    if not isinstance(coord, list):
        if coord['type'] == 'Feature' and coord['geometry'] and coord['geometry']['type'] == 'Point':
            return coord['geometry']['coordinates']

        if coord['type'] == 'Point':
            return coord['coordinates']

    if isinstance(coord, list) and len(coord) >= 2 and not isinstance(coord[0], list) and not isinstance(coord[1],
                                                                                                         list):
        return coord

    raise Exception('coord must be GeoJSON Point or an Array of numbers')


def get_geom(geojson):
    if geojson['type'] == 'Feature':
        return geojson['geometry']
    return geojson


def get_coords(coords):
    if isinstance(coords, list): return coords

    if coords['type'] == 'Feature':
        if coords['geometry']: return coords['geometry']['coordinates']
    else:
        if coords['coordinates']:
            return coords['coordinates']
    raise Exception('coords must be GeoJSON Feature, Geometry Object or an List')


def feature_of(feature, type, name):
    if not feature:
        raise Exception('No feature passed')

    if not name:
        raise Exception('.featureOf() requires a name')

    if not feature or feature['type'] != 'Feature' or not feature['geometry']:
        raise Exception('Invalid input to ' + str(name) + ', Feature with geometry required')

    if not feature['geometry'] or feature['geometry']['type'] != type:
        raise Exception('Invalid input to ' + name + ': must be a ' + type + ', given ' + feature['geometry']['type'])

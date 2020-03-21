from math import sin, pi
from geojson import Feature, LineString

RADIUS = 6378137


def geom_reduce(geojson, initial_value_param):
    initial_value = initial_value_param
    previous_value = initial_value_param

    def callback_geom_each(current_geometry, feature_index, feature_properties, feature_bbox, feature_id):
        nonlocal initial_value
        nonlocal previous_value

        def callback_geom_reduce(value, geom):
            return value + calculate_area(geom)

        if feature_index == 0 and initial_value:
            previous_value = current_geometry
        else:
            previous_value = callback_geom_reduce(previous_value, current_geometry)
        return previous_value

    geom_each(geojson, callback_geom_each)
    return previous_value


def geom_each(geojson, callback):
    """
    Iterate over each geometry in any GeoJSON object, similar to Array.forEach()
    :param geojson: Point|Polygon|MultiPolygon|MultiPoint|LineString|MultiLineString|FeatureCollection|Feature geojson any GeoJSON object
    :param callback:
    :return:
    """
    feature_index = 0
    is_feature_collection = geojson['type'] == 'FeatureCollection'
    is_feature = geojson['type'] == 'Feature'
    stop = len(geojson['features']) if is_feature_collection else 1

    for i in range(0, stop):
        if is_feature_collection:
            geometry_maybe_collection = geojson['features'][i]['geometry']
            feature_properties = geojson['features'][i].get('properties')
            feature_b_box = geojson['features'][i].get('bbox')
            feature_id = geojson['features'][i].get('id')
        elif is_feature:
            geometry_maybe_collection = geojson['geometry']
            feature_properties = geojson.get('properties')
            feature_b_box = geojson.get('bbox')
            feature_id = geojson.get('id')
        else:
            geometry_maybe_collection = geojson
            feature_properties = {}
            feature_b_box = None
            feature_id = None

        if geometry_maybe_collection:
            if geometry_maybe_collection['type'] == 'GeometryCollection':
                is_geometry_collection = True
            else:
                is_geometry_collection = False
        stop_g = len(geometry_maybe_collection['geometries']) if is_geometry_collection else 1

        for g in range(0, stop_g):
            geometry = geometry_maybe_collection['geometries'][
                g] if is_geometry_collection else geometry_maybe_collection

            if not geometry:
                if not callback(None, feature_index, feature_properties, feature_b_box, feature_id):
                    return False
                continue

            if geometry['type'] == 'Point' \
                    or geometry['type'] == 'LineString' \
                    or geometry['type'] == 'MultiPoint' \
                    or geometry['type'] == 'Polygon' \
                    or geometry['type'] == 'MultiLineString' \
                    or geometry['type'] == 'MultiPolygon':
                if not callback(geometry, feature_index, feature_properties, feature_b_box, feature_id):
                    return False
                break
            elif geometry['type'] == 'GeometryCollection':
                for j in range(0, len(geometry['geometries'])):
                    if not callback(geometry['geometries'][j], feature_index, feature_properties, feature_b_box,
                                    feature_id):
                        return False
                break
            else:
                raise Exception('Unknown Geometry Type')
        feature_index += feature_index + 1


def calculate_area(geom) -> float:
    total = 0
    if geom['type'] == 'Polygon':
        return polygon_area(geom['coordinates'])
    elif geom['type'] == 'MultiPolygon':
        for coords in geom['coordinates']:
            total += polygon_area(coords)
            return total
    elif geom['type'] == 'Point' \
            or geom['type'] == 'MultiPoint' \
            or geom['type'] == 'LineString' \
            or geom['type'] == 'MultiLineString':
        return 0
    return 0


def polygon_area(coords: list):
    total = 0

    if coords and len(coords) > 0:
        total += abs(ring_area(coords[0]))
        for i in range(1, len(coords)):
            total -= abs(ring_area(coords[i]))

    return total


def ring_area(coords: list):
    total = 0
    coords_length = len(coords)

    if coords_length > 2:
        for i in range(0, coords_length):
            if i == coords_length - 2:
                lower_index = coords_length - 2
                middle_index = coords_length - 1
                upper_index = 0
            elif i == coords_length - 1:
                lower_index = coords_length - 1
                middle_index = 0
                upper_index = 1
            else:
                lower_index = i
                middle_index = i + 1
                upper_index = i + 2

            p1 = coords[lower_index]
            p2 = coords[middle_index]
            p3 = coords[upper_index]
            total += (rad(p3[0]) - rad(p1[0])) * sin(rad(p2[1]))

        total = total * RADIUS * RADIUS / 2
    return total


def rad(num: float):
    return num * pi / 180


def coord_each(geojson, callback, excludeWrapCoord=None):
    """
    Iterate over coordinates in any GeoJSON object, similar to Array.forEach()
    :return:
    """
    if not geojson:
        return
    wrap_shrink = 0
    coord_index = 0
    type = geojson['type']
    is_feature_collection = type == 'FeatureCollection'
    is_feature = type == 'Feature'
    stop = len(geojson['features']) if is_feature_collection else 1

    for feature_index in range(0, stop):
        if is_feature_collection:
            geometry_maybe_collection = geojson['features'][feature_index]['geometry']
        elif is_feature:
            geometry_maybe_collection = geojson['geometry']
        else:
            geometry_maybe_collection = geojson

        if geometry_maybe_collection:
            is_geometry_collection = geometry_maybe_collection['type'] == 'GeometryCollection'
        else:
            is_geometry_collection = False

        stopG = len(geometry_maybe_collection['geometries']) if is_geometry_collection else 1

        for geom_index in range(0, stopG):
            multi_feature_index = 0
            geometry_index = 0
            geometry = geometry_maybe_collection['geometries'][
                geom_index] if is_geometry_collection else geometry_maybe_collection

            if not geometry:
                continue
            coords = geometry['coordinates']
            geom_type = geometry['type']

            wrapShrink = 1 if excludeWrapCoord and (geom_type == 'Polygon' or geom_type == 'MultiPolygon') else 0

            if geom_type:
                if geom_type == 'Point':
                    # if not callback(coords):
                    #     return False
                    callback(coords, coord_index, feature_index, multi_feature_index, geometry_index)
                    coord_index += coord_index + 1
                    multi_feature_index += multi_feature_index + 1
                elif geom_type == 'LineString' or geom_type == 'MultiPoint':
                    for j in range(0, len(coords)):
                        # if not callback(coords[j]):
                        #     return False
                        callback(coords[j], coord_index, feature_index, multi_feature_index, geometry_index)
                        coord_index += coord_index + 1
                        if geom_type == 'MultiPoint':
                            multi_feature_index += multi_feature_index + 1
                    if geom_type == 'LineString':
                        multi_feature_index += multi_feature_index + 1
                elif geom_type == 'Polygon' or geom_type == 'MultiLineString':
                    for j in range(0, len(coords)):
                        for k in range(0, len(coords[j]) - wrapShrink):
                            # if not callback(coords[j][k]):
                            #     return False
                            callback(coords[j][k], coord_index, feature_index, multi_feature_index, geometry_index)
                            coord_index += coord_index + 1
                        if geom_type == 'MultiLineString':
                            multi_feature_index += multi_feature_index + 1
                        if geom_type == 'Polygon':
                            geometry_index += geometry_index + 1
                    if geom_type == 'Polygon':
                        multi_feature_index += multi_feature_index + 1
                elif geom_type == 'MultiPolygon':
                    for j in range(0, len(coords)):
                        geometry_index = 0
                        for k in range(0, len(coords[j])):
                            for l in range(0, len(coords[j][k]) - wrapShrink):
                                # if not callback(coords[j][k][l]):
                                #     return False
                                callback(coords[j][k][l], coord_index, feature_index, multi_feature_index,
                                         geometry_index)
                                coord_index += coord_index + 1
                            geometry_index += geometry_index + 1
                        multi_feature_index += multi_feature_index + 1
                elif geom_type == 'GeometryCollection':
                    for j in range(0, len(geometry['geometries'])):
                        if not coord_each(geometry['geometries'][j], callback, excludeWrapCoord):
                            return False
                else:
                    raise Exception('Unknown Geometry Type')


def segment_reduce(geojson, callback, initial_value=None):
    previous_value = initial_value
    started = False

    def callback_segment_each(current_segment, feature_index, multi_feature_index, geometry_index, segment_index):
        nonlocal started
        nonlocal previous_value
        if not started and (not initial_value and initial_value != 0):
            previous_value = current_segment
        else:
            previous_value = callback(previous_value, current_segment)
        started = True
        return True

    segment_each(geojson, callback_segment_each)

    return previous_value


def segment_each(geojson, callback):
    def callback_flatten_each(feature, feature_index, multi_feature_index):
        segment_index = 0

        if not feature['geometry']:
            return

        type = feature['geometry']['type']

        if type == 'Point' or type == 'MultiPoint':
            return

        previous_coords = None
        previous_feature_index = 0
        previous_multi_index = 0
        prev_geom_index = 0

        def callback_coord_each(current_coord, coord_index, feature_index_coord, multi_part_index_coord,
                                geometry_index):
            nonlocal previous_coords
            nonlocal previous_feature_index
            nonlocal previous_multi_index
            nonlocal prev_geom_index
            nonlocal segment_index
            if not previous_coords or feature_index > previous_feature_index or multi_part_index_coord > previous_multi_index or geometry_index > prev_geom_index:
                previous_coords = current_coord
                previous_feature_index = feature_index
                previous_multi_index = multi_part_index_coord
                prev_geom_index = geometry_index
                segment_index = 0
                return
            ls = LineString([previous_coords, current_coord])
            current_segment = Feature(geometry=ls, properties=feature['properties'] if feature['properties'] else {})
            if not callback(current_segment, feature_index, multi_feature_index, geometry_index, segment_index):
                return False
            segment_index = segment_index + 1
            previous_coords = current_coord

        if not coord_each(feature, callback_coord_each):
            return False

    flatten_each(geojson, callback_flatten_each)


def flatten_each(geojson, callback):
    def callback_geom_each(geometry, feature_index, properties, bbox, id):
        if not geometry:
            type = None
        else:
            type = geometry['type']

        if not type or type == 'Point' or type == 'LineString' or type == 'Polygon':
            if not callback(Feature(geometry=geometry, bbox=bbox, id=id), feature_index, 0):
                return False
            return True

        geom_type = ''

        if type == 'MultiPoint':
            geom_type = 'Point'
        elif type == 'MultiLineString':
            geom_type = 'LineString'
        elif type == 'MultiPolygon':
            geom_type = 'Polygon'

        for multi_feature_index in range(0, len(geometry['coordinates'])):
            coordinate = geometry['coordinates'][multi_feature_index]
            geom = {
                'type': geom_type,
                'coordinates': coordinate
            }
            if not callback(Feature(geometry=geom, properties=properties), feature_index, multi_feature_index):
                return False
        return True

    geom_each(geojson, callback_geom_each)


def feature_each(geojson, callback):
    if geojson['type'] == 'Feature':
        callback(geojson, 0)
    elif geojson['type'] == 'FeatureCollection':
        for i in range(0, len(geojson['features'])):
            if not callback(geojson['features'][i], i):
                break

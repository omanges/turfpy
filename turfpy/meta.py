from math import pi, sin

from geojson import Feature, LineString, Point

RADIUS = 6378137


def coord_each(geojson_obj, callback, exclude_wrap_coord=False):
    if geojson_obj is None:
        return

    coord_index = 0
    is_feature_collection = geojson_obj["type"] == "FeatureCollection"
    is_feature = geojson_obj["type"] == "Feature"

    stop = len(geojson_obj["features"]) if is_feature_collection else 1

    for feature_index in range(stop):
        geometry_maybe_collection = (
            geojson_obj["features"][feature_index]["geometry"]
            if is_feature_collection
            else geojson_obj["geometry"] if is_feature else geojson_obj
        )
        is_geometry_collection = (
            geometry_maybe_collection["type"] == "GeometryCollection"
            if geometry_maybe_collection
            else False
        )
        stop_g = (
            len(geometry_maybe_collection["geometries"]) if is_geometry_collection else 1
        )

        for geom_index in range(stop_g):
            multi_feature_index = 0
            geometry_index = 0
            geometry = (
                geometry_maybe_collection["geometries"][geom_index]
                if is_geometry_collection
                else geometry_maybe_collection
            )
            if geometry is None:
                continue

            coords = geometry["coordinates"]
            geom_type = geometry["type"]
            wrap_shrink = (
                1
                if exclude_wrap_coord
                and (geom_type == "Polygon" or geom_type == "MultiPolygon")
                else 0
            )

            if geom_type == "Point":
                if (
                    callback(
                        coords,
                        coord_index,
                        feature_index,
                        multi_feature_index,
                        geometry_index,
                    )
                    is False
                ):
                    return False
                coord_index += 1
                multi_feature_index += 1
            elif geom_type in ["LineString", "MultiPoint"]:
                for j in range(len(coords)):
                    if (
                        callback(
                            coords[j],
                            coord_index,
                            feature_index,
                            multi_feature_index,
                            geometry_index,
                        )
                        is False
                    ):
                        return False
                    coord_index += 1
                    if geom_type == "MultiPoint":
                        multi_feature_index += 1
                if geom_type == "LineString":
                    multi_feature_index += 1
            elif geom_type in ["Polygon", "MultiLineString"]:
                for j in range(len(coords)):
                    for k in range(len(coords[j]) - wrap_shrink):
                        if (
                            callback(
                                coords[j][k],
                                coord_index,
                                feature_index,
                                multi_feature_index,
                                geometry_index,
                            )
                            is False
                        ):
                            return False
                        coord_index += 1
                    if geom_type == "MultiLineString":
                        multi_feature_index += 1
                    if geom_type == "Polygon":
                        geometry_index += 1
                if geom_type == "Polygon":
                    multi_feature_index += 1
            elif geom_type == "MultiPolygon":
                for j in range(len(coords)):
                    geometry_index = 0
                    for k in range(len(coords[j])):
                        for m in range(len(coords[j][k]) - wrap_shrink):
                            if (
                                callback(
                                    coords[j][k][m],
                                    coord_index,
                                    feature_index,
                                    multi_feature_index,
                                    geometry_index,
                                )
                                is False
                            ):
                                return False
                            coord_index += 1
                        geometry_index += 1
                    multi_feature_index += 1
            elif geom_type == "GeometryCollection":
                for j in range(len(geometry["geometries"])):
                    if (
                        coord_each(
                            geometry["geometries"][j], callback, exclude_wrap_coord
                        )
                        is False
                    ):
                        return False
            else:
                raise ValueError("Unknown Geometry Type")


def coord_reduce(geojson_obj, callback, initial_value=None, exclude_wrap_coord=False):
    previous_value = initial_value

    def _callback(*args):
        nonlocal previous_value
        (
            current_coord,
            coord_index,
            feature_index,
            multi_feature_index,
            geometry_index,
        ) = args
        if coord_index == 0 and initial_value is None:
            previous_value = current_coord
        else:
            previous_value = callback(
                previous_value,
                current_coord,
                coord_index,
                feature_index,
                multi_feature_index,
                geometry_index,
            )

    coord_each(geojson_obj, _callback, exclude_wrap_coord)
    return previous_value


def prop_each(geojson_obj, callback):
    if geojson_obj["type"] == "FeatureCollection":
        for i, feature in enumerate(geojson_obj["features"]):
            if callback(feature["properties"], i) is False:
                break
    elif geojson_obj["type"] == "Feature":
        callback(geojson_obj["properties"], 0)


def prop_reduce(geojson_obj, callback, initial_value=None):
    previous_value = initial_value

    def _callback(current_properties, feature_index):
        nonlocal previous_value
        if feature_index == 0 and initial_value is None:
            previous_value = current_properties
        else:
            previous_value = callback(previous_value, current_properties, feature_index)

    prop_each(geojson_obj, _callback)
    return previous_value


def feature_each(geojson_obj, callback):
    if geojson_obj["type"] == "Feature":
        callback(geojson_obj, 0)
    elif geojson_obj["type"] == "FeatureCollection":
        for i, feature in enumerate(geojson_obj["features"]):
            if callback(feature, i) is False:
                break


def feature_reduce(geojson_obj, callback, initial_value=None):
    previous_value = initial_value

    def _callback(current_feature, feature_index):
        nonlocal previous_value
        if feature_index == 0 and initial_value is None:
            previous_value = current_feature
        else:
            previous_value = callback(previous_value, current_feature, feature_index)

    feature_each(geojson_obj, _callback)
    return previous_value


def coord_all(geojson_obj):
    coords = []

    def _callback(coord, *args):
        coords.append(coord)

    coord_each(geojson_obj, _callback)
    return coords


def geom_each(geojson_obj, callback):
    feature_index = 0
    is_feature_collection = geojson_obj["type"] == "FeatureCollection"
    is_feature = geojson_obj["type"] == "Feature"
    stop = len(geojson_obj["features"]) if is_feature_collection else 1

    for i in range(stop):
        geometry_maybe_collection = (
            geojson_obj["features"][i]["geometry"]
            if is_feature_collection
            else geojson_obj["geometry"] if is_feature else geojson_obj
        )
        feature_properties = (
            geojson_obj["features"][i]["properties"]
            if is_feature_collection
            else geojson_obj["properties"] if is_feature else {}
        )
        feature_bbox = (
            geojson_obj["features"][i].get("bbox")
            if is_feature_collection
            else geojson_obj.get("bbox") if is_feature else None
        )
        feature_id = (
            geojson_obj["features"][i].get("id")
            if is_feature_collection
            else geojson_obj.get("id") if is_feature else None
        )
        is_geometry_collection = (
            geometry_maybe_collection["type"] == "GeometryCollection"
            if geometry_maybe_collection
            else False
        )
        stop_g = (
            len(geometry_maybe_collection["geometries"]) if is_geometry_collection else 1
        )

        for g in range(stop_g):
            geometry = (
                geometry_maybe_collection["geometries"][g]
                if is_geometry_collection
                else geometry_maybe_collection
            )
            if geometry is None:
                if (
                    callback(
                        None,
                        feature_index,
                        feature_properties,
                        feature_bbox,
                        feature_id,
                    )
                    is False
                ):
                    return False
                continue

            if geometry["type"] in [
                "Point",
                "LineString",
                "MultiPoint",
                "Polygon",
                "MultiLineString",
                "MultiPolygon",
            ]:
                if (
                    callback(
                        geometry,
                        feature_index,
                        feature_properties,
                        feature_bbox,
                        feature_id,
                    )
                    is False
                ):
                    return False
            elif geometry["type"] == "GeometryCollection":
                for geom in geometry["geometries"]:
                    if (
                        callback(
                            geom,
                            feature_index,
                            feature_properties,
                            feature_bbox,
                            feature_id,
                        )
                        is False
                    ):
                        return False
            else:
                raise ValueError("Unknown Geometry Type")

        feature_index += 1


def rad(num: float):
    return num * pi / 180

def ring_area(coords: list):
    total = 0.0
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


def polygon_area(coords: list) -> float:
    total = 0

    if coords and len(coords) > 0:
        total += abs(ring_area(coords[0]))
        for i in range(1, len(coords)):
            total -= abs(ring_area(coords[i]))

    return total


def calculate_area(geom) -> float:
    total = 0.0
    if geom["type"] == "Polygon":
        return polygon_area(geom["coordinates"])
    elif geom["type"] == "MultiPolygon":
        for coords in geom["coordinates"]:
            total += polygon_area(coords)
        return total
    elif (
        geom["type"] == "Point"
        or geom["type"] == "MultiPoint"
        or geom["type"] == "LineString"
        or geom["type"] == "MultiLineString"
    ):
        return 0
    return 0

def geom_reduce(geojson, initial_value_param):
    initial_value = initial_value_param
    previous_value = initial_value_param

    def callback_geom_each(
        current_geometry,
        feature_index,
        feature_properties,
        feature_bbox,
        feature_id,
    ):
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


def flatten_each(geojson_obj, callback):
    def _flatten_callback(geometry, feature_index, properties, bbox, id_):
        geom_type = None
        if geometry is not None:
            geom_type = geometry["type"]
        if geom_type in [None, "Point", "LineString", "Polygon"]:
            if (
                callback(
                    Feature(geometry=geometry, properties=properties, bbox=bbox, id=id_),
                    feature_index,
                    0,
                )
                is False
            ):
                return False
            return

        geom_type_mapping = {
            "MultiPoint": "Point",
            "MultiLineString": "LineString",
            "MultiPolygon": "Polygon",
        }
        geom_type = geom_type_mapping[geom_type]

        for multi_feature_index, coordinates in enumerate(geometry["coordinates"]):
            geom = {"type": geom_type, "coordinates": coordinates}
            if (
                callback(
                    Feature(geometry=geom, properties=properties),
                    feature_index,
                    multi_feature_index,
                )
                is False
            ):
                return False

    geom_each(geojson_obj, _flatten_callback)


def flatten_reduce(geojson_obj, callback, initial_value=None):
    previous_value = initial_value

    def _callback(current_feature, feature_index, multi_feature_index):
        nonlocal previous_value
        if feature_index == 0 and multi_feature_index == 0 and initial_value is None:
            previous_value = current_feature
        else:
            previous_value = callback(
                previous_value, current_feature, feature_index, multi_feature_index
            )

    flatten_each(geojson_obj, _callback)
    return previous_value


def segment_each(geojson_obj, callback):
    def _segment_callback(feature, feature_index, multi_feature_index):
        segment_index = 0
        if feature["geometry"] is None:
            return
        geom_type = feature["geometry"]["type"]
        if geom_type in ["Point", "MultiPoint"]:
            return

        previous_coords = None
        previous_feature_index = 0
        previous_multi_index = 0
        prev_geom_index = 0

        def _coord_callback(
            current_coord,
            coord_index,
            feature_index_coord,
            multi_part_index_coord,
            geometry_index,
        ):
            nonlocal previous_coords
            nonlocal previous_feature_index
            nonlocal previous_multi_index
            nonlocal prev_geom_index
            nonlocal segment_index
            if (
                previous_coords is None
                or feature_index > previous_feature_index
                or multi_part_index_coord > previous_multi_index
                or geometry_index > prev_geom_index
            ):
                previous_coords = current_coord
                previous_feature_index = feature_index
                previous_multi_index = multi_part_index_coord
                prev_geom_index = geometry_index
                segment_index = 0
                return

            current_segment = LineString(
                [previous_coords, current_coord], properties=feature["properties"]
            )
            if (
                callback(
                    current_segment,
                    feature_index,
                    multi_feature_index,
                    geometry_index,
                    segment_index,
                )
                is False
            ):
                return False
            segment_index += 1
            previous_coords = current_coord

        coord_each(feature, _coord_callback)

    flatten_each(geojson_obj, _segment_callback)


def segment_reduce(geojson_obj, callback, initial_value=None):
    previous_value = initial_value
    started = False

    def _callback(
        current_segment,
        feature_index,
        multi_feature_index,
        geometry_index,
        segment_index,
    ):
        nonlocal previous_value, started
        if not started and initial_value is None:
            previous_value = current_segment
        else:
            previous_value = callback(
                previous_value,
                current_segment,
                feature_index,
                multi_feature_index,
                geometry_index,
                segment_index,
            )
        started = True

    segment_each(geojson_obj, _callback)
    return previous_value


def line_each(geojson_obj, callback):
    if not geojson_obj:
        raise ValueError("geojson is required")

    def _line_callback(feature, feature_index, multi_feature_index):
        if feature["geometry"] is None:
            return
        geom_type = feature["geometry"]["type"]
        coords = feature["geometry"]["coordinates"]

        if geom_type == "LineString":
            if callback(feature, feature_index, multi_feature_index, 0, 0) is False:
                return False
        elif geom_type == "Polygon":
            for geometry_index, line_coords in enumerate(coords):
                if (
                    callback(
                        LineString(line_coords, properties=feature["properties"]),
                        feature_index,
                        multi_feature_index,
                        geometry_index,
                    )
                    is False
                ):
                    return False

    flatten_each(geojson_obj, _line_callback)


def line_reduce(geojson_obj, callback, initial_value=None):
    previous_value = initial_value

    def _callback(current_line, feature_index, multi_feature_index, geometry_index):
        nonlocal previous_value
        if feature_index == 0 and initial_value is None:
            previous_value = current_line
        else:
            previous_value = callback(
                previous_value,
                current_line,
                feature_index,
                multi_feature_index,
                geometry_index,
            )

    line_each(geojson_obj, _callback)
    return previous_value


def find_segment(geojson_obj, options):
    if not isinstance(options, dict):
        raise ValueError("options is invalid")

    feature_index = options.get("featureIndex", 0)
    multi_feature_index = options.get("multiFeatureIndex", 0)
    geometry_index = options.get("geometryIndex", 0)
    segment_index = options.get("segmentIndex", 0)
    properties = options.get("properties")

    geometry = None
    if geojson_obj["type"] == "FeatureCollection":
        if feature_index < 0:
            feature_index = len(geojson_obj["features"]) + feature_index
        properties = properties or geojson_obj["features"][feature_index]["properties"]
        geometry = geojson_obj["features"][feature_index]["geometry"]
    elif geojson_obj["type"] == "Feature":
        properties = properties or geojson_obj["properties"]
        geometry = geojson_obj["geometry"]
    elif geojson_obj["type"] in ["Point", "MultiPoint"]:
        return None
    elif geojson_obj["type"] in [
        "LineString",
        "Polygon",
        "MultiLineString",
        "MultiPolygon",
    ]:
        geometry = geojson_obj
    else:
        raise ValueError("geojson is invalid")

    if geometry is None:
        return None

    coords = geometry["coordinates"]
    if geometry["type"] == "Point" or geometry["type"] == "MultiPoint":
        return None
    elif geometry["type"] == "LineString":
        if segment_index < 0:
            segment_index = len(coords) + segment_index - 1
        return LineString(
            [coords[segment_index], coords[segment_index + 1]], properties=properties
        )
    elif geometry["type"] == "Polygon":
        if geometry_index < 0:
            geometry_index = len(coords) + geometry_index
        if segment_index < 0:
            segment_index = len(coords[geometry_index]) + segment_index - 1
        return LineString(
            [
                coords[geometry_index][segment_index],
                coords[geometry_index][segment_index + 1],
            ],
            properties=properties,
        )
    elif geometry["type"] == "MultiLineString":
        if multi_feature_index < 0:
            multi_feature_index = len(coords) + multi_feature_index
        if segment_index < 0:
            segment_index = len(coords[multi_feature_index]) + segment_index - 1
        return LineString(
            [
                coords[multi_feature_index][segment_index],
                coords[multi_feature_index][segment_index + 1],
            ],
            properties=properties,
        )
    elif geometry["type"] == "MultiPolygon":
        if multi_feature_index < 0:
            multi_feature_index = len(coords) + multi_feature_index
        if geometry_index < 0:
            geometry_index = len(coords[multi_feature_index]) + geometry_index
        if segment_index < 0:
            segment_index = (
                len(coords[multi_feature_index][geometry_index]) - segment_index - 1
            )
        return LineString(
            [
                coords[multi_feature_index][geometry_index][segment_index],
                coords[multi_feature_index][geometry_index][segment_index + 1],
            ],
            properties=properties,
        )
    else:
        raise ValueError("geojson is invalid")


def find_point(geojson_obj, options):
    if not isinstance(options, dict):
        raise ValueError("options is invalid")

    feature_index = options.get("featureIndex", 0)
    multi_feature_index = options.get("multiFeatureIndex", 0)
    geometry_index = options.get("geometryIndex", 0)
    coord_index = options.get("coordIndex", 0)
    properties = options.get("properties")

    geometry = None
    if geojson_obj["type"] == "FeatureCollection":
        if feature_index < 0:
            feature_index = len(geojson_obj["features"]) + feature_index
        properties = properties or geojson_obj["features"][feature_index]["properties"]
        geometry = geojson_obj["features"][feature_index]["geometry"]
    elif geojson_obj["type"] == "Feature":
        properties = properties or geojson_obj["properties"]
        geometry = geojson_obj["geometry"]
    elif geojson_obj["type"] in ["Point", "MultiPoint"]:
        return None
    elif geojson_obj["type"] in [
        "LineString",
        "Polygon",
        "MultiLineString",
        "MultiPolygon",
    ]:
        geometry = geojson_obj
    else:
        raise ValueError("geojson is invalid")

    if geometry is None:
        return None

    coords = geometry["coordinates"]
    if geometry["type"] == "Point":
        return Point(coords, properties=properties)
    elif geometry["type"] == "MultiPoint":
        if multi_feature_index < 0:
            multi_feature_index = len(coords) + multi_feature_index
        return Point(coords[multi_feature_index], properties=properties)
    elif geometry["type"] == "LineString":
        if coord_index < 0:
            coord_index = len(coords) + coord_index
        return Point(coords[coord_index], properties=properties)
    elif geometry["type"] == "Polygon":
        if geometry_index < 0:
            geometry_index = len(coords) + geometry_index
        if coord_index < 0:
            coord_index = len(coords[geometry_index]) + coord_index
        return Point(coords[geometry_index][coord_index], properties=properties)
    elif geometry["type"] == "MultiLineString":
        if multi_feature_index < 0:
            multi_feature_index = len(coords) + multi_feature_index
        if coord_index < 0:
            coord_index = len(coords[multi_feature_index]) + coord_index
        return Point(coords[multi_feature_index][coord_index], properties=properties)
    elif geometry["type"] == "MultiPolygon":
        if multi_feature_index < 0:
            multi_feature_index = len(coords) + multi_feature_index
        if geometry_index < 0:
            geometry_index = len(coords[multi_feature_index]) + geometry_index
        if coord_index < 0:
            coord_index = len(coords[multi_feature_index][geometry_index]) + coord_index
        return Point(
            coords[multi_feature_index][geometry_index][coord_index],
            properties=properties,
        )

    raise ValueError("geojson is invalid")

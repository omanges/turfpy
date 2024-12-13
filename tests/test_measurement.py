import json

from geojson import (
    Feature,
    FeatureCollection,
    GeometryCollection,
    LineString,
    MultiLineString,
    MultiPoint,
    MultiPolygon,
    Point,
    Polygon,
)

from turfpy.measurement import (
    along,
    area,
    bbox,
    bbox_polygon,
    center,
    destination,
    envelope,
    length,
    midpoint,
    nearest_point,
    point_to_line_distance,
    rhumb_bearing,
    rhumb_destination,
    rhumb_distance,
    square,
)

def test_area():
    """Test area function."""
    geometry_1 = {"coordinates": [[[0, 0], [0, 10], [10, 10], [10, 0], [0, 0]]], "type": "Polygon"};
    geometry_2 = {"coordinates": [[[2.38, 57.322], [23.194, -20.28], [-120.43, 19.15], [2.38, 57.322]]], "type": "Polygon"};
    feature_1 = Feature(geometry=geometry_1)
    feature_2 = Feature(geometry=geometry_2)
    feature_collection = FeatureCollection([feature_1, feature_2])

    assert area(feature_collection) == 56837434206665.02


def test_bbox_point():
    p = Point((-75.343, 39.984))
    bb = bbox(p)
    assert bb[0] == -75.343
    assert bb[1] == 39.984
    assert bb[2] == -75.343
    assert bb[3] == 39.984


def test_bbox_multi_point():
    mp = MultiPoint([(-155.52, 19.61), (-156.22, 20.74), (-157.97, 21.46)])
    bb = bbox(mp)
    assert bb[0] == -157.97
    assert bb[1] == 19.61
    assert bb[2] == -155.52
    assert bb[3] == 21.46


def test_bbox_line_string():
    ls = LineString([(8.919, 44.4074), (8.923, 44.4075)])
    bb = bbox(ls)
    assert bb[0] == 8.919
    assert bb[1] == 44.4074
    assert bb[2] == 8.923
    assert bb[3] == 44.4075


def test_bbox_multi_line_string():
    mls = MultiLineString(
        (
            [(3.75, 9.25), (-130.95, 1.52)],
            [(23.15, -34.25), (-1.35, -4.65), (3.45, 77.95)],
        )
    )
    bb = bbox(mls)
    assert bb[0] == -130.95
    assert bb[1] == -34.25
    assert bb[2] == 23.15
    assert bb[3] == 77.95


def test_bbox_polygon():
    p = Polygon([[(2.38, 57.322), (23.194, -20.28), (-120.43, 19.15), (2.38, 57.322)]])
    bb = bbox(p)
    assert bb[0] == -120.43
    assert bb[1] == -20.28
    assert bb[2] == 23.194
    assert bb[3] == 57.322


def test_bbox_multi_polygon():
    mp = MultiPolygon(
        [
            ([(3.78, 9.28), (-130.91, 1.52), (35.12, 72.234), (3.78, 9.28)],),
            (
                [
                    (23.18, -34.29),
                    (-1.31, -4.61),
                    (3.41, 77.91),
                    (23.18, -34.29),
                ],
            ),
        ]
    )
    bb = bbox(mp)
    assert bb[0] == -130.91
    assert bb[1] == -34.29
    assert bb[2] == 35.12
    assert bb[3] == 77.91


def test_bbox_geometry_collection():
    my_point = Point((23.532, -63.12))
    my_line = LineString([(-152.62, 51.21), (5.21, 10.69)])
    geo_collection = GeometryCollection([my_point, my_line])
    bb = bbox(geo_collection)
    assert bb[0] == -152.62
    assert bb[1] == -63.12
    assert bb[2] == 23.532
    assert bb[3] == 51.21


def test_bbox_feature():
    my_line = LineString([(-152.62, 51.21), (5.21, 10.69)])
    f = Feature(geometry=my_line)
    bb = bbox(f)
    assert bb[0] == -152.62
    assert bb[1] == 10.69
    assert bb[2] == 5.21
    assert bb[3] == 51.21


def test_feature_collection():
    line1_feature = Feature(geometry=LineString([(8.919, 44.4074), (8.923, 44.4075)]))
    line2_feature = Feature(geometry=LineString([(-152.62, 51.21), (5.21, 10.69)]))
    fc = FeatureCollection([line1_feature, line2_feature])
    bb = bbox(fc)
    assert bb[0] == -152.62
    assert bb[1] == 10.69
    assert bb[2] == 8.923
    assert bb[3] == 51.21


def test_bbox_polygon_feature():
    p = Polygon([[(2.38, 57.322), (23.194, -20.28), (-120.43, 19.15), (2.38, 57.322)]])
    bbox_poly = bbox_polygon(bbox(p))
    assert bbox_poly["geometry"]["coordinates"] == [
        [
            [-120.43, -20.28],
            [23.194, -20.28],
            [23.194, 57.322],
            [-120.43, 57.322],
            [-120.43, -20.28],
        ]
    ]


def test_center_feature():
    f1 = Feature(geometry=Point((-97.522259, 35.4691)))
    f2 = Feature(geometry=Point((-97.502754, 35.463455)))
    f3 = Feature(geometry=Point((-97.508269, 35.463245)))
    feature_collection = FeatureCollection([f1, f2, f3])
    feature = center(feature_collection)
    assert feature["geometry"]["coordinates"] == [-97.512507, 35.466172]


def test_envelope():
    f1 = Feature(geometry=Point((-75.343, 39.984)))
    f2 = Feature(geometry=Point((-75.833, 39.284)))
    f3 = Feature(geometry=Point((-75.534, 39.123)))
    feature_collection = FeatureCollection([f1, f2, f3])
    feature = envelope(feature_collection)
    assert feature["geometry"]["coordinates"] == [
        [
            [-75.833, 39.123],
            [-75.343, 39.123],
            [-75.343, 39.984],
            [-75.833, 39.984],
            [-75.833, 39.123],
        ]
    ]


def test_rhumb_destination():
    start = Feature(geometry=Point((-75.343, 39.984)), properties={"marker-color": "F00"})
    distance = 50
    bearing = 90
    dest = rhumb_destination(
        start,
        distance,
        bearing,
        {"units": "mi", "properties": {"marker-color": "F00"}},
    )
    assert dest["geometry"]["coordinates"] == [-74.398553, 39.984]


def test_rhumb_distnace():
    start = Feature(geometry=Point((-75.343, 39.984)))
    end = Feature(geometry=Point((-75.534, 39.123)))
    dis = rhumb_distance(start, end, "mi")
    assert round(dis, 4) == 60.3533


def test_square():
    bbox = [-20, -20, -15, 0]
    res = square(bbox)
    assert res == [-27.5, -20, -7.5, 0]


def test_along():
    ls = LineString([(-83, 30), (-84, 36), (-78, 41)])
    res = along(ls, 200, "mi")
    assert res["type"] == "Feature"
    assert res["geometry"]["type"] == "Point"
    c0, c1 = list(map(lambda x: round(x, 4), res["geometry"]["coordinates"]))
    assert c0 == -83.4609
    assert c1 == 32.8678


def test_midpoint():
    point1 = Feature(geometry=Point((144.834823, -37.771257)))
    point2 = Feature(geometry=Point((145.14244, -37.830937)))
    mp = midpoint(point1, point2)
    assert mp["type"] == "Feature"
    assert mp["geometry"]["type"] == "Point"
    c0, c1 = list(map(lambda x: round(x, 4), mp["geometry"]["coordinates"]))
    assert c0 == 144.9886
    assert c1 == -37.8012


def test_nearest_point():
    f1 = Feature(geometry=Point((28.96991729736328, 41.01190001748873)))
    f2 = Feature(geometry=Point((28.948459, 41.024204)))
    f3 = Feature(geometry=Point((28.938674, 41.013324)))
    fc = FeatureCollection([f1, f2, f3])
    t = Feature(geometry=Point((28.973865, 41.011122)))
    np = nearest_point(t, fc)
    assert np["type"] == "Feature"
    assert np["geometry"]["type"] == "Point"
    c0, c1 = list(map(lambda x: round(x, 4), np["geometry"]["coordinates"]))
    assert c0 == 28.9699
    assert c1 == 41.0119


def test_length():
    ls = LineString([(115, -32), (131, -22), (143, -25), (150, -34)])
    lens = length(ls, units="mi")
    assert round(lens, 4) == 2738.9664


def test_destination():
    origin = Feature(geometry=Point((-75.343, 39.984)))
    distance = 50
    bearing = 90
    options = {"units": "mi"}
    des = destination(origin, distance, bearing, options)
    assert des["type"] == "Feature"
    assert des["geometry"]["type"] == "Point"
    c0, c1 = list(map(lambda x: round(x, 4), des["geometry"]["coordinates"]))
    assert c0 == -74.3986
    assert c1 == 39.9802


def test_point_to_line_distance():
    point = Feature(geometry=Point((0, 0)))
    linestring = Feature(geometry=LineString([(1, 1), (-1, 1)]))
    pld = point_to_line_distance(point, linestring, units="mi")
    assert round(pld, 4) == 69.0934


def test_rhumb_bearing():
    start = Feature(geometry=Point((-75.343, 39.984)))
    end = Feature(geometry=Point((-75.534, 39.123)))
    rhb = rhumb_bearing(start, end)
    assert round(rhb, 4) == -170.2942


# def test_polygon_tangents():
#     point = Feature(geometry=Point([61, 5]))
#     polygon = Feature(geometry=Polygon([[(11, 0), (22, 4), (31, 0), (31, 11),
#                                              (21, 15), (11, 11), (11, 0)]]))
#     pt = polygon_tangents(point, polygon)
#     print(pt)

# def test_point_on_feature():
#     point = Polygon([[(116, -36), (131, -32), (146, -43), (155, -25), (133, -9),
#     (111, -22), (116, -36)]])
#     feature = Feature(geometry=point)
#     pn = point_on_feature(feature)
#     print(pn)

# def test_centroid():
#     polygon = Polygon([[(-81, 41), (-88, 36), (-84, 31), (-80, 33), (-77, 39),
#     (-81, 41)]])
#     cen = centroid(polygon)
#     assert cen["type"] == "Feature"
#     assert cen["geometry"]["type"] == "Point"
#     c0, c1 = cen["geometry"]["coordinates"]
#     # assert c0 == 82
#     assert c1 == 36

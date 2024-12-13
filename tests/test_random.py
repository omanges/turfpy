"""
Test module for randoms.
"""

from geojson import Feature, Point

from turfpy.boolean import boolean_point_in_polygon
from turfpy.measurement import bbox
from turfpy.random import random_points, random_position


def test_random_position():
    data = {
        "type": "Feature",
        "properties": {},
        "geometry": {
            "type": "Polygon",
            "coordinates": [
                [
                    [11.953125, 18.979025953255267],
                    [52.03125, 18.979025953255267],
                    [52.03125, 46.558860303117164],
                    [11.953125, 46.558860303117164],
                    [11.953125, 18.979025953255267],
                ]
            ],
        },
    }

    pos = random_position(bbox=bbox(data))
    assert len(pos) == 2
    pos = Feature(geometry=Point(pos))
    assert boolean_point_in_polygon(point=pos, polygon=data)


def test_random_points():
    data = {
        "type": "Feature",
        "properties": {},
        "geometry": {
            "type": "Polygon",
            "coordinates": [
                [
                    [11.953125, 18.979025953255267],
                    [52.03125, 18.979025953255267],
                    [52.03125, 46.558860303117164],
                    [11.953125, 46.558860303117164],
                    [11.953125, 18.979025953255267],
                ]
            ],
        },
    }

    pos = random_points(count=3, bbox=bbox(data))
    assert len(pos["features"]) == 3
    for point in pos["features"]:
        assert boolean_point_in_polygon(point=point, polygon=data)

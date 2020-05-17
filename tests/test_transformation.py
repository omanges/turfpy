"""
Test module for transformations.
"""
from geojson import Feature, Point

from turfpy.transformation import circle


def test_circle():
    center = Feature(geometry=Point((-75.343, 39.984)))
    cc = circle(center, radius=5, steps=10)
    assert cc.type == "Polygon"
    assert len(cc.coordinates) == 11
    assert cc.coordinates == [
        [-75.343, 40.028966],
        [-75.398824, 39.997882],
        [-75.377476, 39.947617],
        [-75.308524, 39.947617],
        [-75.287176, 39.997882],
        [-75.343, 40.028966],
        [-75.398824, 39.997882],
        [-75.377476, 39.947617],
        [-75.308524, 39.947617],
        [-75.287176, 39.997882],
        [-75.343, 40.028966],
    ]

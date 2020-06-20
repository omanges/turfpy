"""
Test module for transformations.
"""
from geojson import Feature, Point

from turfpy.transformation import circle, bbox_clip


def test_circle():
    center = Feature(geometry=Point((-75.343, 39.984)))
    cc = circle(center, radius=5, steps=10)
    cc = cc['geometry']
    assert cc.type == "Polygon"
    assert len(cc.coordinates[0]) == 11
    assert cc.coordinates == [[
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
    ]]


def test_bbox_clip():
    f = Feature(geometry={"coordinates": [[[2, 2], [8, 4], [12, 8], [3, 7], [2, 2]]], "type": "Polygon"})
    bbox = [0, 0, 10, 10]
    clip = bbox_clip(f, [0, 0, 10, 10])
    clip = clip['geometry']
    assert clip.type == "Polygon"
    assert len(clip.coordinates[0]) == 6
    assert clip.coordinates == [[[10.0, 7.777778],
         [10.0, 6.0],
         [8.0, 4.0],
         [2.0, 2.0],
         [3.0, 7.0],
         [10.0, 7.777778]
    ]]
"""
Test module for transformations.
"""
from geojson import Feature, Point, LineString

from turfpy.transformation import circle, bbox_clip, intersect, bezie_spline


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
    clip = bbox_clip(f, bbox)
    clip = clip['geometry']
    assert clip.type == "Polygon"
    assert len(clip.coordinates[0]) == 6
    assert clip.coordinates == [[[10.0, 6.0],
                                 [8.0, 4.0],
                                 [2.0, 2.0],
                                 [3.0, 7.0],
                                 [10.0, 7.777778],
                                 [10.0, 6.0]]]


def test_intersection():
    f = Feature(geometry={"coordinates": [
        [[-122.801742, 45.48565], [-122.801742, 45.60491],
         [-122.584762, 45.60491], [-122.584762, 45.48565],
         [-122.801742, 45.48565]]], "type": "Polygon"})
    b = Feature(geometry={"coordinates": [
        [[-122.520217, 45.535693], [-122.64038, 45.553967],
         [-122.720031, 45.526554], [-122.669906, 45.507309],
         [-122.723464, 45.446643], [-122.532577, 45.408574],
         [-122.487258, 45.477466], [-122.520217, 45.535693]
         ]], "type": "Polygon"})
    inter = intersect(f, b)
    inter = inter['geometry']
    assert inter.type == "Polygon"
    assert len(inter.coordinates[0]) == 7
    assert inter.coordinates == [[[-122.584762, 45.545509],
                                  [-122.584762, 45.48565],
                                  [-122.689027, 45.48565],
                                  [-122.669906, 45.507309],
                                  [-122.720031, 45.526554],
                                  [-122.64038, 45.553967],
                                 [-122.584762, 45.545509]]]


def test_bezie_spline():
    ls = LineString([(-76.091308, 18.427501), (-76.695556, 18.729501), (-76.552734, 19.40443), (-74.61914, 19.134789),
                     (-73.652343, 20.07657), (-73.157958, 20.210656)])

    f = Feature(geometry=ls)

    bf = bezie_spline(f)
    bf = bf['geometry']
    assert bf.type == "LineString"
    assert len(bf.coordinates) == 500

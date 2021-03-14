from geojson import Feature, LineString, Point
from pytest import approx

from turfpy.misc import line_intersect, line_segment, line_slice, nearest_point_on_line


def test_line_intersect():
    l1 = Feature(geometry=LineString([[126, -11], [129, -21]]))
    l2 = Feature(geometry=LineString([[123, -18], [131, -14]]))

    li = line_intersect(l1, l2)

    assert li["type"] == "FeatureCollection"
    assert len(li["features"]) == 1
    assert li["features"][0]["geometry"]["coordinates"] == [127.434783, -15.782609]


def test_line_segment():
    poly = {
        "type": "Feature",
        "properties": {},
        "geometry": {
            "type": "Polygon",
            "coordinates": [
                [
                    [51.17431640625, 47.025206001585396],
                    [45.17578125, 43.13306116240612],
                    [54.5361328125, 41.85319643776675],
                    [51.17431640625, 47.025206001585396],
                ]
            ],
        },
    }

    segments = line_segment(poly)

    assert segments["type"] == "FeatureCollection"
    assert len(segments["features"]) == 3
    assert segments["features"] == [
        {
            "bbox": [45.175781, 43.133061, 51.174316, 47.025206],
            "geometry": {
                "coordinates": [[45.175781, 43.133061], [51.174316, 47.025206]],
                "type": "LineString",
            },
            "id": 0,
            "properties": {},
            "type": "Feature",
        },
        {
            "bbox": [45.175781, 41.853196, 54.536133, 43.133061],
            "geometry": {
                "coordinates": [[54.536133, 41.853196], [45.175781, 43.133061]],
                "type": "LineString",
            },
            "id": 1,
            "properties": {},
            "type": "Feature",
        },
        {
            "bbox": [51.174316, 41.853196, 54.536133, 47.025206],
            "geometry": {
                "coordinates": [[51.174316, 47.025206], [54.536133, 41.853196]],
                "type": "LineString",
            },
            "id": 2,
            "properties": {},
            "type": "Feature",
        },
    ]


def test_nearest_point_on_line():
    pt = Point([2.5, 1.75])
    ls = Feature(geometry=LineString([(1, 2), (2, 2), (3, 2)]))
    opts = {"key1": "value1", "key2": "value2"}

    npl = nearest_point_on_line(ls, pt, options={"properties": opts.copy()})

    assert npl.geometry["type"] == "Point"
    assert npl.properties["index"] == 1
    assert 27.798 == approx(npl.properties["dist"], abs=1e-3)
    assert 166.682 == approx(npl.properties["location"], abs=1e-3)
    assert npl.geometry.coordinates == approx([2.5, 2], abs=1e-3)
    for key in opts.keys():
        assert npl.properties[key] == opts[key]


def test_line_slice():
    start = Point([1.5, 1.5])
    stop = Point([4.5, 1.5])
    line = Feature(geometry=LineString([[1, 1], [2, 2], [3, 1], [4, 2], [5, 1]]))

    sliced = line_slice(start, stop, line)

    assert sliced.geometry["type"] == "LineString"
    assert len(sliced.geometry["coordinates"]) == 5
    crds = line.geometry.coordinates
    crds[0] = start.coordinates
    crds[4] = stop.coordinates
    ref_crds = [i for crd in crds for i in crd]
    sliced_crds = [i for crd in sliced.geometry.coordinates for i in crd]
    assert sliced_crds == approx(ref_crds, abs=1e-3)

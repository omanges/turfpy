from geojson import Feature, LineString

from turfpy.misc import line_intersect, line_segment


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

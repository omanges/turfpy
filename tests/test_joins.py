from geojson import Feature, FeatureCollection, MultiPolygon, Point, Polygon

from turfpy.joins import points_within_polygon


def test_points_within_polygon():
    f1 = Feature(geometry=Point((-46.6318, -23.5523)))
    f2 = Feature(geometry=Point((-46.6246, -23.5325)))
    f3 = Feature(geometry=Point((-46.6062, -23.5513)))
    f4 = Feature(geometry=Point((-46.663, -23.554)))
    f5 = Feature(geometry=Point((-46.643, -23.557)))
    f6 = Feature(geometry=Point((-73, 45)))
    f7 = Feature(geometry=Point((36, 71)))
    points = FeatureCollection([f1, f2, f3, f4, f5, f6, f7])
    poly = Polygon(
        [
            [
                (-46.653, -23.543),
                (-46.634, -23.5346),
                (-46.613, -23.543),
                (-46.614, -23.559),
                (-46.631, -23.567),
                (-46.653, -23.560),
                (-46.653, -23.543),
            ]
        ]
    )
    fpoly = Feature(geometry=poly)
    poly2 = Polygon(
        [
            [
                (-76.653, -11.543),
                (-46.634, -23.5346),
                (-46.613, -23.543),
                (-46.614, -23.559),
                (-46.631, -23.567),
                (-46.653, -23.560),
                (-76.653, -11.543),
            ]
        ]
    )
    fpoly2 = Feature(geometry=poly2)
    fc = FeatureCollection([fpoly, fpoly2])
    result = points_within_polygon(points, fc)
    assert len(result["features"]) == 3

    multi_polygon = Feature(
        geometry=MultiPolygon(
            [
                ([(-81, 41), (-81, 47), (-72, 47), (-72, 41), (-81, 41)],),
                ([(3.78, 9.28), (-130.91, 1.52), (35.12, 72.234), (3.78, 9.28)],),
            ]
        )
    )
    result2 = points_within_polygon(f6, multi_polygon)
    assert result2 == {
        "features": [
            {
                "geometry": {"coordinates": [-73, 45], "type": "Point"},
                "properties": {},
                "type": "Feature",
            }
        ],
        "type": "FeatureCollection",
    }

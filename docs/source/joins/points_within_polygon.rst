Points within Polygon
=====================
Takes two inputs Point/Points and Polygon(s)/MultiPolygon(s) and returns all the Points with in Polygon(s)/MultiPolygon(s).


Interactive Example
-------------------

.. jupyter-execute::

    from geojson import Feature, FeatureCollection, Point, Polygon
    from turfpy.joins import points_within_polygon
    from ipyleaflet import Map, GeoJSON

    p1 = Feature(geometry=Point((-46.6318, -23.5523)))
    p2 = Feature(geometry=Point((-46.6246, -23.5325)))
    p3 = Feature(geometry=Point((-46.6062, -23.5513)))
    p4 = Feature(geometry=Point((-46.663, -23.554)))
    p5 = Feature(geometry=Point((-46.643, -23.557)))

    points = FeatureCollection([p1, p2, p3, p4, p5])

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

    m = Map(center=(-23.5523, -46.6318), zoom=13)
    fc = FeatureCollection([p1, p2, p3, p4, p5, poly])

    geo_json = GeoJSON(
        data=fc,
        style={"opacity": 1, "dashArray": "9", "fillOpacity": 0.3, "weight": 1},
        hover_style={"color": "green", "dashArray": "0", "fillOpacity": 0.5},
    )
    m.add_layer(geo_json)

    result = points_within_polygon(points, poly)

    data = result.copy()
    data["features"].append(Feature(geometry=poly))

    m = Map(center=(-23.5523, -46.6318), zoom=13)

    geo_json2 = GeoJSON(
        data=data,
        style={"opacity": 1, "dashArray": "9", "fillOpacity": 0.3, "weight": 1},
        hover_style={"color": "green", "dashArray": "0", "fillOpacity": 0.5},
    )
    m.add_layer(geo_json2)
    m
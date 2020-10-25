Union
=====
Given list of features or FeatureCollection return union of those.

Example
-------

.. jupyter-execute::

    import json
    from turfpy.transformation import union
    from geojson import Feature, Polygon, FeatureCollection
    f1 = Feature(geometry=Polygon([[
        [-82.574787, 35.594087],
        [-82.574787, 35.615581],
        [-82.545261, 35.615581],
        [-82.545261, 35.594087],
         [-82.574787, 35.594087]
    ]]), properties={"fill": "#00f"})
    f2 = Feature(geometry=Polygon([[
        [-82.560024, 35.585153],
        [-82.560024, 35.602602],
        [-82.52964, 35.602602],
        [-82.52964, 35.585153],
        [-82.560024, 35.585153]]]), properties={"fill": "#00f"})
    un = union(FeatureCollection([f1, f2], properties={"combine": "yes"}))
    print(json.dumps(un, indent=2, sort_keys=True))




Interactive Example
-------------------

.. jupyter-execute::

    from geojson import Feature, Polygon, FeatureCollection
    from ipyleaflet import Map, GeoJSON, LayersControl
    from turfpy.transformation import union

    f1 = Feature(
        geometry=Polygon(
            [
                [
                    [-82.574787, 35.594087],
                    [-82.574787, 35.615581],
                    [-82.545261, 35.615581],
                    [-82.545261, 35.594087],
                    [-82.574787, 35.594087],
                ]
            ]
        ),
        properties={"fill": "#00f"},
    )
    f2 = Feature(
        geometry=Polygon(
            [
                [
                    [-82.560024, 35.585153],
                    [-82.560024, 35.602602],
                    [-82.52964, 35.602602],
                    [-82.52964, 35.585153],
                    [-82.560024, 35.585153],
                ]
            ]
        ),
        properties={"fill": "#00f"},
    )

    geo_json_1 = GeoJSON(name="First Polygon", data=f1)

    geo_json_2 = GeoJSON(name="Second Polygon", data=f2, style={"color": "green"})

    geojson = GeoJSON(
        name="Union",
        data=union(FeatureCollection([f1, f2], properties={"combine": "yes"})),
        style={"color": "red"},
    )

    m = Map(center=[35.60069336198429, -82.54892796278001], zoom=13)
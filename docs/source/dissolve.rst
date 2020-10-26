Dissolve
=========
Take FeatureCollection or list of features to dissolve based on property_name provided.

Example
-------

.. jupyter-execute::

    import json
    from geojson import Polygon, Feature, FeatureCollection
    from turfpy.transformation import dissolve
    f1 = Feature(geometry=Polygon([[
        [0, 0],
        [0, 1],
        [1, 1],
        [1, 0],
        [0, 0]]]), properties={"combine": "yes", "fill": "#00f"})
    f2 = Feature(geometry=Polygon([[
        [0, -1],
        [0, 0],
        [1, 0],
        [1, -1],
        [0,-1]]]), properties={"combine": "yes"})
    f3 = Feature(geometry=Polygon([[
        [1,-1],
        [1, 0],
        [2, 0],
        [2, -1],
        [1, -1]]]), properties={"combine": "no"})
    ds = dissolve(FeatureCollection([f1, f2, f3]), property_name='combine')
    print(json.dumps(ds, indent=2, sort_keys=True))




Interactive Example
-------------------

.. jupyter-execute::

    from geojson import Feature, Polygon, FeatureCollection
    from ipyleaflet import Map, GeoJSON, LayersControl
    from turfpy.transformation import dissolve

    f1 = Feature(
        geometry=Polygon([[[0, 0], [0, 1], [1, 1], [1, 0], [0, 0]]]),
        properties={"combine": "yes", "fill": "#00f"},
    )
    f2 = Feature(
        geometry=Polygon([[[0, -1], [0, 0], [1, 0], [1, -1], [0, -1]]]),
        properties={"combine": "yes"},
    )
    f3 = Feature(
        geometry=Polygon([[[1, -1], [1, 0], [2, 0], [2, -1], [1, -1]]]),
        properties={"combine": "no"},
    )

    geo_json_1 = GeoJSON(name="First Polygon", data=f1)

    geo_json_2 = GeoJSON(name="Second Polygon", data=f2, style={"color": "green"})

    geo_json_3 = GeoJSON(name="Third Polygon", data=f3, style={"color": "black"})

    geojson = GeoJSON(
        name="Dissolve",
        data=dissolve(FeatureCollection([f1, f2, f3]), property_name="combine"),
        style={"color": "red"},
    )


    m = Map(center=[0.257748688144287, 1.9686126708984377], zoom=7)


    m.add_layer(geo_json_1)
    m.add_layer(geo_json_2)
    m.add_layer(geo_json_3)
    m.add_layer(geojson)

    control = LayersControl(position="topright")
    m.add_control(control)

    m
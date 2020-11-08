Difference
==========
Find the difference between given two features.

Example
-------

.. jupyter-execute::

    import json
    from geojson import Polygon, Feature
    from turfpy.transformation import difference
    f1 = Feature(geometry=Polygon([[
        [128, -26],
        [141, -26],
        [141, -21],
        [128, -21],
        [128, -26]]]), properties={"combine": "yes", "fill": "#00f"})
    f2 = Feature(geometry=Polygon([[
        [126, -28],
        [140, -28],
        [140, -20],
        [126, -20],
        [126, -28]]]), properties={"combine": "yes"})
    diff = difference(f1, f2)
    print(json.dumps(diff, indent=2, sort_keys=True))




Interactive Example
-------------------

.. jupyter-execute::

    from geojson import Feature, Polygon, FeatureCollection
    from ipyleaflet import Map, GeoJSON, LayersControl
    from turfpy.transformation import difference

    f1 = Feature(geometry=Polygon([[
        [128, -26],
        [141, -26],
        [141, -21],
        [128, -21],
        [128, -26]]]), properties={"combine": "yes", "fill": "#00f"})
    f2 = Feature(geometry=Polygon([[
        [126, -28],
        [140, -28],
        [140, -20],
        [126, -20],
        [126, -28]]]), properties={"combine": "yes"})

    geo_json_1 = GeoJSON(name="First Polygon", data=f1)

    geo_json_2 = GeoJSON(name='Second Polygon', data=f2, style={'color': 'green'})

    geojson = GeoJSON(name='Difference', data=difference(f1, f2), style={'color': 'red'})


    m = Map(center=[-22.71491497943416, 135.750846862793], zoom=5)


    m.add_layer(geo_json_1)
    m.add_layer(geo_json_2)
    m.add_layer(geojson)

    control = LayersControl(position='topright')
    m.add_control(control)

    m
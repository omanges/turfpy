Envelop
=======
Takes any number of features and returns a rectangular Polygon that encompasses all vertices.


Example
-------

.. jupyter-execute::

    import json
    from turfpy.measurement import envelope
    from geojson import Feature, FeatureCollection, Point

    f1 = Feature(geometry=Point((-97.522259, 35.4691)))
    f2 = Feature(geometry=Point((-97.502754, 35.463455)))
    f3 = Feature(geometry=Point((-97.508269, 35.463245)))
    feature_collection = FeatureCollection([f1, f2, f3])
    print(json.dumps(envelope(feature_collection), indent=2, sort_keys=True))


Interactive Example
-------------------

.. jupyter-execute::

    from turfpy.measurement import envelope
    from geojson import Feature, FeatureCollection, Point
    from ipyleaflet import Map, GeoJSON, WidgetControl, LayersControl

    f1 = Feature(geometry=Point((-97.522259, 35.4691)))
    f2 = Feature(geometry=Point((-97.502754, 35.463455)))
    f3 = Feature(geometry=Point((-97.508269, 35.463245)))
    feature_collection = FeatureCollection([f1, f2, f3])


    m = Map(center=[35.467146770097315, -97.50865470618012], zoom=15)

    geo_json = GeoJSON(name="Geojson", data=feature_collection)
    envelope_geojson = GeoJSON(
        name="Envelope", data=envelope(feature_collection), style={"color": "red"}
    )

    control = LayersControl(position="topright")
    m.add_control(control)

    m.add_layer(geo_json)
    m.add_layer(envelope_geojson)
    m


Center
======
Takes a Feature or FeatureCollection and returns the absolute center point of all features.

Example
-------

.. jupyter-execute::

    import json
    from turfpy.measurement import center
    from geojson import Feature, FeatureCollection, Point

    f1 = Feature(geometry=Point((-97.522259, 35.4691)))
    f2 = Feature(geometry=Point((-97.502754, 35.463455)))
    f3 = Feature(geometry=Point((-97.508269, 35.463245)))
    feature_collection = FeatureCollection([f1, f2, f3])
    print(json.dumps(center(feature_collection), indent=2, sort_keys=True))




Interactive Example
-------------------

.. jupyter-execute::

    from turfpy.measurement import center
    from geojson import Feature, FeatureCollection, Point
    from ipyleaflet import Map, GeoJSON, WidgetControl, LayersControl, CircleMarker

    f1 = Feature(geometry=Point((-97.522259, 35.4691)))
    f2 = Feature(geometry=Point((-97.502754, 35.463455)))
    f3 = Feature(geometry=Point((-97.508269, 35.463245)))
    feature_collection = FeatureCollection([f1, f2, f3])

    m = Map(center=[35.467146770097315, -97.50865470618012], zoom=15)

    geo_json = GeoJSON(name="Geojson", data=feature_collection)

    centre_coord = center(feature_collection)["geometry"]["coordinates"]
    circle_marker = CircleMarker(name="Center")
    circle_marker.location = (centre_coord[1], centre_coord[0])
    circle_marker.radius = 30
    circle_marker.color = "red"

    control = LayersControl(position="topright")
    m.add_control(control)

    m.add_layer(geo_json)
    m.add_layer(circle_marker)
    m


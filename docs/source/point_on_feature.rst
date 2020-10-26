Point On Feature
================
Takes a Feature or FeatureCollection and returns a Point guaranteed to be on the surface of the feature.


Example
-------

.. jupyter-execute::

    import json
    from turfpy.measurement import point_on_feature
    from geojson import  Polygon, Feature
    point = Polygon([[(116, -36), (131, -32), (146, -43), (155, -25), (133, -9), (111, -22), (116, -36)]])
    feature = Feature(geometry=point)
    print(json.dumps(point_on_feature(feature), indent=2, sort_keys=True))




Interactive Example
-------------------

.. jupyter-execute::

    from turfpy.measurement import point_on_feature
    from geojson import  Polygon, Feature
    from ipyleaflet import Map, GeoJSON, LayersControl

    point = Polygon([[(116, -36), (131, -32), (146, -43), (155, -25), (133, -9), (111, -22), (116, -36)]])
    feature = Feature(geometry=point)


    m = Map(center=[-25.743003105825967, 135.92525482177737], zoom=4)

    geo_json = GeoJSON(name='Feature', data=feature)

    m.add_layer(geo_json)

    point_geojson = GeoJSON(name='Point on Feature', data=point_on_feature(feature))

    m.add_layer(point_geojson)

    control = LayersControl(position='topright')
    m.add_control(control)

    m


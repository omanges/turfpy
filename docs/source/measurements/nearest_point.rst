Nearest Point
=============
Takes a reference Point Feature and FeatureCollection of point features and returns the point from the FeatureCollection closest to the reference Point Feature.


Example
-------

.. jupyter-execute::

    import json
    from turfpy.measurement import nearest_point
    from geojson import Point, Feature, FeatureCollection
    f1 = Feature(geometry=Point([28.96991729736328,41.01190001748873]))
    f2 = Feature(geometry=Point([28.948459, 41.024204]))
    f3 = Feature(geometry=Point([28.938674, 41.013324]))
    fc = FeatureCollection([f1, f2 ,f3])
    t = Feature(geometry=Point([28.973865, 41.011122]))
    print(json.dumps(nearest_point(t ,fc), indent=2, sort_keys=True))



Interactive Example
-------------------

.. jupyter-execute::

    from turfpy.measurement import nearest_point
    from geojson import Point, Feature, FeatureCollection
    from ipyleaflet import Map, GeoJSON, LayersControl

    f1 = Feature(geometry=Point([28.96991729736328, 41.01190001748873]))
    f2 = Feature(geometry=Point([28.948459, 41.024204]))
    f3 = Feature(geometry=Point([28.938674, 41.013324]))
    fc = FeatureCollection([f1, f2, f3])
    t = Feature(geometry=Point([28.973865, 41.011122]))


    m = Map(center=[41.01656246584522, 28.959988430142406], zoom=14)

    geo_json = GeoJSON(name="Feature Collection", data=FeatureCollection([f2, f3]))

    ref_geo_json = GeoJSON(name="Reference Point", data=t)

    m.add_layer(geo_json)

    m.add_layer(ref_geo_json)

    near_geojson = GeoJSON(name="Nearest Point", data=nearest_point(t, fc))
    m.add_layer(near_geojson)

    control = LayersControl(position="topright")
    m.add_control(control)

    m


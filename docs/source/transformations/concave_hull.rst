Concave Hull
============

Generate concave hull for the given feature or Feature Collection.

Example
-------

.. jupyter-execute::

    import json
    from turfpy.transformation import concave
    from geojson import FeatureCollection, Feature, Point
    f1 = Feature(geometry=Point((-63.601226, 44.642643)))
    f2 = Feature(geometry=Point((-63.591442, 44.651436)))
    f3 = Feature(geometry=Point((-63.580799, 44.648749)))
    f4 = Feature(geometry=Point((-63.573589, 44.641788)))
    f5 = Feature(geometry=Point((-63.587665, 44.64533)))
    f6 = Feature(geometry=Point((-63.595218, 44.64765)))
    fc = [f1, f2, f3, f4, f5, f6]
    ch = concave(FeatureCollection(fc), alpha=100)
    print(json.dumps(ch, indent=2, sort_keys=True))



Interactive Example
-------------------

.. jupyter-execute::

    from geojson import FeatureCollection, Feature, Point
    from ipyleaflet import Map, GeoJSON
    from turfpy.transformation import concave

    f1 = Feature(geometry=Point((-63.601226, 44.642643)))
    f2 = Feature(geometry=Point((-63.591442, 44.651436)))
    f3 = Feature(geometry=Point((-63.580799, 44.648749)))
    f4 = Feature(geometry=Point((-63.573589, 44.641788)))
    f5 = Feature(geometry=Point((-63.587665, 44.64533)))
    f6 = Feature(geometry=Point((-63.595218, 44.64765)))
    fc = [f1, f2, f3, f4, f5, f6]
    fc = FeatureCollection(fc)

    geo_json = GeoJSON(data=fc)

    spline_geo_json = GeoJSON(data=concave(FeatureCollection(fc), alpha=100), style={'color': 'red'})

    m = Map(center=[44.64740465397292, -63.58361206948757], zoom=14)

    m.add_layer(geo_json)
    m.add_layer(spline_geo_json)

    m
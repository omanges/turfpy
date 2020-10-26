Bezier spline
=============

Takes a line and returns a curved version by applying a Bezier spline algorithm.

Example
-------

.. jupyter-execute::

    import json
    from geojson import LineString, Feature
    from turfpy.transformation import bezier_spline
    ls = LineString([(-76.091308, 18.427501),
                        (-76.695556, 18.729501),
                        (-76.552734, 19.40443),
                        (-74.61914, 19.134789),
                        (-73.652343, 20.07657),
                        (-73.157958, 20.210656)])
    f = Feature(geometry=ls)
    bs = bezier_spline(f)
    print(json.dumps(bs, indent=2, sort_keys=True))



Interactive Example
-------------------

.. jupyter-execute::

    from geojson import LineString, Feature
    from ipyleaflet import Map, GeoJSON
    from turfpy.transformation import bezier_spline

    ls = LineString([(-76.091308, 18.427501),
                        (-76.695556, 18.729501),
                        (-76.552734, 19.40443),
                        (-74.61914, 19.134789),
                        (-73.652343, 20.07657),
                        (-73.157958, 20.210656)])
    f = Feature(geometry=ls)


    geo_json = GeoJSON(data=f)

    spline_geo_json = GeoJSON(data=bezier_spline(f), style={'color': 'red'})

    m = Map(center=[19.318170089962457, -74.85710620880128], zoom=8)

    m.add_layer(geo_json)
    m.add_layer(spline_geo_json)

    m
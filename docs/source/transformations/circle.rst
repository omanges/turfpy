Circle
======
Takes a Point and calculates the circle polygon given a radius in degrees, radians, miles, or kilometers; and steps for precision.

Example
-------

.. jupyter-execute::

    import json
    from geojson import Feature, Point
    from turfpy.transformation import circle

    center = Feature(geometry=Point((19.0760, 72.8777)))
    cc = circle(center, radius=5, steps=10)
    print(json.dumps(cc, indent=2, sort_keys=True))



Interactive Example
-------------------

.. jupyter-execute::

    from geojson import Point, Feature
    from ipyleaflet import Map, GeoJSON
    from turfpy.transformation import circle

    center = Feature(geometry=Point((-75.343, 39.984)))

    geo_json = GeoJSON(data=circle(center, radius=5, steps=10, units='km'))

    m = Map(center=[39.978756161038504, -75.32421022653581], zoom=11)

    m.add_layer(geo_json)

    m
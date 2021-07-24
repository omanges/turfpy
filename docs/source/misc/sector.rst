Sector
================
Creates a circular sector of a circle of given radius and center Point, between (clockwise) bearing1 and bearing2; 0 bearing is North of center point, positive clockwise.

Example
-------

.. jupyter-execute::

    from turfpy.misc import sector
    from geojson import Feature, Point

    center = Feature(geometry=Point((-75, 40)))
    radius = 5
    bearing1 = 25
    bearing2 = 45

    feature = sector(center, radius, bearing1, bearing2, options={"properties":{"length":3}})



Interactive Example
-------------------

.. jupyter-execute::

    from ipyleaflet import Map, GeoJSON, LayersControl
    from turfpy.misc import sector
    from geojson import Feature, Point, LineString, FeatureCollection

    center = Feature(geometry=Point((-75, 40)))
    radius = 5;
    bearing1 = 25;
    bearing2 = 45;

    m = Map(center=[40.011313056309056, -74.97720068362348], zoom=12)

    feature = sector(center, radius, bearing1, bearing2, options={"properties":{"length":3}})


    fc = FeatureCollection([feature, center])

    layer = GeoJSON(name="Line_Arc", data=fc, style={'color':'red'})

    m.add_layer(layer)
    m


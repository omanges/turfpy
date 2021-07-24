Line Arc
================
Creates a circular arc, of a circle of the given radius and center point, between bearing1 and bearing2; 0 bearing is North of center point, positive clockwise.

Example
-------

.. jupyter-execute::

    from turfpy.misc import line_arc
    from geojson import Feature, Point

    center = Feature(geometry=Point((-75, 40)))
    radius = 5
    bearing1 = 25
    bearing2 = 47

    line_arc(center=center, radius=radius, bearing1=bearing1, bearing2=bearing2)



Interactive Example
-------------------

.. jupyter-execute::

    from ipyleaflet import Map, GeoJSON, LayersControl
    from turfpy.misc import line_arc
    from geojson import Feature, Point, LineString, FeatureCollection

    center = Feature(geometry=Point((-75, 40)))
    radius = 5;
    bearing1 = 25;
    bearing2 = 47;

    m = Map(center=[40.011313056309056, -74.97720068362348], zoom=12)

    feature = line_arc(center=center, radius=radius, bearing1=bearing1, bearing2=bearing2)

    fc = FeatureCollection([feature, center])

    layer = GeoJSON(name="Line_Arc", data=fc, style={'color':'red'})

    m.add_layer(layer)
    m


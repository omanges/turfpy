Line Intersect
================
Takes any LineString or Polygon GeoJSON and returns the intersecting point(s). If one of the Features is polygon pass the polygon feature as the first parameter to improve performance. To use this functionality Rtree or pygeos is needed to be installed.

Example
-------

.. jupyter-execute::

    from geojson import LineString, Feature
    from turfpy.misc import line_intersect
    l1 = Feature(geometry=LineString([[126, -11], [129, -21]]))
    l2 = Feature(geometry=LineString([[123, -18], [131, -14]]))
    line_intersect(l1, l2)



Interactive Example
-------------------

.. jupyter-execute::

    from ipyleaflet import Map, GeoJSON
    from geojson import LineString, Feature
    from turfpy.misc import line_intersect

    m = Map(center=[-15.150511712009196, 127.52157211303712], zoom=5)

    l1 = Feature(geometry=LineString([[126, -11], [129, -21]]))

    l2 = Feature(geometry=LineString([[123, -18], [131, -14]]))

    Line1 = GeoJSON(name="Line1", data=l1)
    Line2 = GeoJSON(name="Line2", data=l2)


    m.add_layer(Line1)
    m.add_layer(Line2)

    intersection = GeoJSON(name="intersection", data=line_intersect(l1, l2))
    m.add_layer(intersection)

    m


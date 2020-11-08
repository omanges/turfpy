Rhumb Bearing
=============
Takes two points and finds the bearing angle between them along a Rhumb line i.e. the angle measured in degrees start the north line (0 degrees).


Example
-------

.. jupyter-execute::

    from turfpy.measurement import rhumb_bearing
    from geojson import Feature, Point
    start = Feature(geometry=Point([-75.343, 39.984]))
    end = Feature(geometry=Point([-75.534, 39.123]))
    rhumb_bearing(start, end, True)


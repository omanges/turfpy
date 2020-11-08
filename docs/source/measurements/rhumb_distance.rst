Rhumb Distance
==============
Calculates the distance along a rhumb line between two points in degrees, radians, miles, or kilometers.

Example
-------

.. jupyter-execute::

    from turfpy.measurement import rhumb_distance
    from geojson import Point, Feature
    start = Feature(geometry=Point([-75.343, 39.984]))
    end = Feature(geometry=Point([-75.534, 39.123]))
    rhumb_distance(start, end,'mi')
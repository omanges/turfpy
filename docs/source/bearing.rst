Bearing
=======
Takes two Points and finds the geographic bearing between them.

Example
-------

.. jupyter-execute::

    from turfpy import measurement
    from geojson import Point, Feature

    start = Feature(geometry=Point((-75.343, 39.984)))
    end = Feature(geometry=Point((-75.534, 39.123)))
    measurement.bearing(start, end)
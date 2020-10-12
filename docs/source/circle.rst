Circle
======
Takes a Point and calculates the circle polygon given a radius in degrees, radians, miles, or kilometers; and steps for precision.

Example
-------

.. jupyter-execute::

    from geojson import Feature, Point
    from turfpy.transformation import circle

    center = Feature(geometry=Point((19.0760, 72.8777)))
    circle(center, radius=5, steps=10)
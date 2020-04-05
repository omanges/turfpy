"""
This module impolements some of the spatial analysis techiques and processes used to
understand the patterns and relationships of geographic features.
This is mainly inspired from turf.js.
link: http://turfjs.org/
"""
from geojson import Point, Polygon

from turfpy.measurement import destination


def circle(
    center: Point, radius: int, steps: int = 64, units: str = "km", **kwargs
) -> Polygon:
    """
    Takes a Point and calculates the circle polygon given a radius in degrees,
    radians, miles, or kilometers; and steps for precision.

    :param center: A `Point` object representing center point of circle.
    :param radius: An int representing radius of the circle.
    :param steps: An int representing number of steps.
    :param units: A string representing units of distance e.g. 'mi', 'km',
        'deg' and 'rad'.
    :param kwargs: A dict representing additional properties.
    :return: A polygon object.

    Example:

    >>> from turfpy import circle
    >>> circle(center=Point((-75.343, 39.984)), radius=5, steps=10)

    """
    coordinates = []
    options = dict(steps=steps, units=units)
    options.update(kwargs)
    for i in range(steps):
        bearing = i * -360 / radius
        pt = destination(center, radius, bearing, options=options)
        cords = pt.geometry.coordinates
        coordinates.append(cords)
    coordinates.append(coordinates[0])
    return Polygon(coordinates, **kwargs)

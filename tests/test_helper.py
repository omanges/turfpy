"""
This module will test all functions in helper module.
"""

from geojson import Feature, Point, Polygon

from turfpy.helper import get_coord, get_coords
from turfpy.measurement import distance


def test_get_coord():
    """Test get_coord function."""

    point = Point((73, 19))
    feature = Feature(geometry=point)
    flist = [73, 19]
    c1 = get_coord(point)
    c2 = get_coord(feature)
    c3 = get_coord(flist)
    assert c1 == [73, 19]
    assert c1 == c2 == c3

    # Test for derived class from Feature
    class Vertex(Feature):
        """Derived from Feature"""

        def __init__(self, node: str, point: Point):
            Feature.__init__(self, geometry=point)
            self.nodeid = node

    p1 = Point((25.25458, 51.623879))
    f1 = Feature(geometry=p1)
    v1 = Vertex("v1", point=p1)
    p2 = Point((25.254626, 51.624053))
    f2 = Feature(geometry=p2)
    v2 = Vertex("v2", point=p2)

    df = distance(f1, f2)
    dv = distance(v1, v2)
    assert df == dv


def test_get_coords():
    """Test get_coords function"""
    poly = Polygon([[(2.38, 57.322), (23.194, -20.28), (-120.43, 19.15), (2.38, 57.322)]])
    coords = get_coords(poly)
    assert coords == poly.coordinates

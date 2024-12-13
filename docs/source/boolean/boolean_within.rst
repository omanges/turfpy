Boolean Within 
==============
Boolean-within returns true if the first geometry is completely within the second geometry. The interiors of both geometries must intersect and, the interior and boundary of the primary (geometry a) must not intersect the exterior of the secondary (geometry b).

Example
-------

.. jupyter-execute::

    from geojson import Feature, Point, Polygon
    from turfpy.boolean import boolean_within

    poly = Polygon(
        [
            [
                (1, 1),
                (1, 10),
                (10, 10),
                (10, 1),
                (1, 1)
            ]
        ]
    )

    feature_1 = Feature(geometry=Point((4, 4)))
    feature_2 = Feature(geometry=poly)
    boolean_within(feature_1, feature_2)


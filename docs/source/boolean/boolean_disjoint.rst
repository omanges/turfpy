Boolean Disjoint 
=============
Takes two features and returns (TRUE) if the two geometries do not touch or overlap.


Example
-------

.. jupyter-execute::

    from geojson import Feature, Point
    from turfpy.boolean import boolean_disjoint

    feature_1 = Feature(geometry=Point((19.0760, 72.8777)))
    feature_2 = Feature(geometry=Point((29.0760, 72.8777)))
    boolean_disjoint(feature_1, feature_2)

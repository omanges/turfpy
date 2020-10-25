Rhumb Destination
=================
Returns the destination Point having travelled the given distance along a Rhumb line from the origin Point with the (varant) given bearing.


Example
-------

.. jupyter-execute::

    import json
    from turfpy.measurement import rhumb_destination
    from geojson import Point, Feature
    start = Feature(geometry=Point([-75.343, 39.984]), properties={"marker-color": "F00"})
    distance = 50
    bearing = 90
    rd = rhumb_destination(start, distance, bearing, {'units':'mi', 'properties': {"marker-color": "F00"}})
    print(json.dumps(rd, indent=2, sort_keys=True))

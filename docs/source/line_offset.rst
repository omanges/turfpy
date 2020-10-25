Line Offset
===========
Takes a linestring or multilinestring and returns a line at offset by the specified distance.


Example
-------

.. jupyter-execute::

    import json
    from geojson import MultiLineString, Feature
    from turfpy.transformation import line_offset
    ls = Feature(geometry=MultiLineString([
         [(3.75, 9.25), (-130.95, 1.52)],
         [(23.15, -34.25), (-1.35, -4.65), (3.45, 77.95)]
     ]))
    lo = line_offset(ls, 2, unit='mi')
    print(json.dumps(lo, indent=2, sort_keys=True))



Interactive Example
-------------------

.. jupyter-execute::

    from ipyleaflet import Map, GeoJSON, LayersControl

    original = GeoJSON(name='Original', data=ls)

    rotated = GeoJSON(name='Offset Line', data=line_offset(ls, 2, unit='mi'), style={'color': 'red'})

    m = Map(center=[33.54139466898275, 7.536621093750001], zoom=1)

    m.add_layer(original)
    m.add_layer(rotated)

    control = LayersControl(position='topright')
    m.add_control(control)
    m

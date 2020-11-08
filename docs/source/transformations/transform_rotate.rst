Transform Rotate
================
Rotates any geojson Feature or Geometry of a specified angle, around its centroid or a given pivot point; all rotations follow the right-hand rule.


Example
-------

.. jupyter-execute::

    import json
    from turfpy.transformation import transform_rotate
    from geojson import Polygon, Feature
    f = Feature(geometry=Polygon([[[0,29],[3.5,29],[2.5,32],[0,29]]]))
    pivot = [0, 25]
    tr = transform_rotate(f, 10, pivot)
    print(json.dumps(tr, indent=2, sort_keys=True))


Interactive Example
-------------------

.. jupyter-execute::

    from ipyleaflet import Map, GeoJSON, LayersControl

    original = GeoJSON(name='Original', data=f)

    rotated = GeoJSON(name='Rotated', data=transform_rotate(f, 10, pivot), style={'color': 'red'})

    m = Map(center=[30.18519925274955, 2.939529418945313], zoom=5)

    m.add_layer(original)
    m.add_layer(rotated)

    control = LayersControl(position='topright')
    m.add_control(control)
    m
Transform Translate
===================
Moves any geojson Feature or Geometry of a specified distance along a Rhumb Line on the provided direction angle.


Example
-------

.. jupyter-execute::

    import json
    from turfpy.transformation import transform_translate
    from geojson import Polygon, Feature
    f = Feature(geometry=Polygon([[[0,29],[3.5,29],[2.5,32],[0,29]]]))
    tt = transform_translate(f, 100, direction=35, mutate=True)
    print(json.dumps(tt, indent=2, sort_keys=True))



Interactive Example
-------------------

.. jupyter-execute::

    from ipyleaflet import Map, GeoJSON, LayersControl

    original = GeoJSON(name='Original', data=f)

    rotated = GeoJSON(name='Translated', data=transform_translate(f, 100, 35, mutate=True), style={'color': 'red'})

    m = Map(center=[30.18519925274955, 2.939529418945313], zoom=5)

    m.add_layer(original)
    m.add_layer(rotated)

    control = LayersControl(position='topright')
    m.add_control(control)
    m

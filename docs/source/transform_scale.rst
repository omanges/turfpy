Transform Scale
===============
Scale a GeoJSON from a given point by a factor of scaling (ex: factor=2 would make the GeoJSON 200% larger). If a FeatureCollection is provided, the origin point will be calculated based on each individual Feature.

Example
-------

.. jupyter-execute::

    import json
    from turfpy.transformation import transform_scale
    from geojson import Polygon, Feature
    f = Feature(geometry=Polygon([[[0,29],[3.5,29],[2.5,32],[0,29]]]))
    ts = transform_scale(f, 3, origin=[0, 29])
    print(json.dumps(ts, indent=2, sort_keys=True))




Interactive Example
-------------------

.. jupyter-execute::

    from ipyleaflet import Map, GeoJSON, LayersControl

    original = GeoJSON(name='Original', data=f)

    rotated = GeoJSON(name='Scaled', data=transform_scale(f, 3, origin=[0, 29]), style={'color': 'red'})

    m = Map(center=[33.52608402076209, 7.55413055419922], zoom=5)

    m.add_layer(original)
    m.add_layer(rotated)

    control = LayersControl(position='topright')
    m.add_control(control)
    m
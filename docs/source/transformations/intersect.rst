Intersect
=========
Takes polygons and finds their intersection.


Example
-------

.. jupyter-execute::

    import json
    from turfpy.transformation import intersect
    from geojson import Feature
    f = Feature(geometry={"coordinates": [
    [[-122.801742, 45.48565], [-122.801742, 45.60491],
    [-122.584762, 45.60491], [-122.584762, 45.48565],
    [-122.801742, 45.48565]]], "type": "Polygon"})
    b = Feature(geometry={"coordinates": [
    [[-122.520217, 45.535693], [-122.64038, 45.553967],
    [-122.720031, 45.526554], [-122.669906, 45.507309],
    [-122.723464, 45.446643], [-122.532577, 45.408574],
    [-122.487258, 45.477466], [-122.520217, 45.535693]
    ]], "type": "Polygon"})
    it = intersect([f, b])
    print(json.dumps(it, indent=2, sort_keys=True))




Interactive Example
-------------------

.. jupyter-execute::

    from geojson import Feature
    from ipyleaflet import Map, GeoJSON, LayersControl
    from turfpy.transformation import intersect

    f = Feature(geometry={"coordinates": [
    [[-122.801742, 45.48565], [-122.801742, 45.60491],
    [-122.584762, 45.60491], [-122.584762, 45.48565],
    [-122.801742, 45.48565]]], "type": "Polygon"})
    b = Feature(geometry={"coordinates": [
    [[-122.520217, 45.535693], [-122.64038, 45.553967],
    [-122.720031, 45.526554], [-122.669906, 45.507309],
    [-122.723464, 45.446643], [-122.532577, 45.408574],
    [-122.487258, 45.477466], [-122.520217, 45.535693]
    ]], "type": "Polygon"})

    geo_json_1 = GeoJSON(name="First Polygon", data=f)

    geo_json_2 = GeoJSON(name='Second Polygon', data=b, style={'color': 'green'})

    geojson = GeoJSON(name='Intersection', data=intersect([f, b]), style={'color': 'red'})


    m = Map(center=[45.510343157077976, -122.63075172901155], zoom=10)

    m.add_layer(geo_json_1)
    m.add_layer(geo_json_2)
    m.add_layer(geojson)

    control = LayersControl(position='topright')
    m.add_control(control)

    m

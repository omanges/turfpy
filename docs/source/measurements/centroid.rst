Centroid
========
Takes one or more features and calculates the centroid using the mean of all vertices.


Example
-------

.. jupyter-execute::

    import json
    from turfpy.measurement import centroid
    from geojson import Polygon
    polygon = Polygon([[(-81, 41), (-88, 36), (-84, 31), (-80, 33), (-77, 39), (-81, 41)]])
    print(json.dumps(centroid(polygon), indent=2, sort_keys=True))


Interactive Example
-------------------

.. jupyter-execute::

    from turfpy.measurement import centroid
    from geojson import Polygon, Feature
    from ipyleaflet import Map, GeoJSON, WidgetControl, LayersControl

    polygon = Polygon([[(-81, 41), (-88, 36), (-84, 31), (-80, 33), (-77, 39), (-81, 41)]])

    m = Map(center=[36.198988385375806, -79.6392059326172], zoom=5)

    geo_json = GeoJSON(name="Geojson", data=Feature(geometry=polygon))
    centroid_geojson = GeoJSON(name="Centroid", data=centroid(polygon))

    control = LayersControl(position="topright")
    m.add_control(control)

    m.add_layer(geo_json)
    m.add_layer(centroid_geojson)
    m


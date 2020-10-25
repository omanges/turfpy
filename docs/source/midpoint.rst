Midpoint
========
Get midpoint between any the two points.


Example
-------

.. jupyter-execute::

    import json
    from turfpy.measurement import midpoint
    from geojson import Point, Feature
    point1 = Feature(geometry=Point([144.834823, -37.771257]))
    point2 = Feature(geometry=Point([145.14244, -37.830937]))
    print(json.dumps(midpoint(point1, point2), indent=2, sort_keys=True))



Interactive Example
-------------------

.. jupyter-execute::

    from turfpy.measurement import midpoint
    from geojson import Point, Feature
    from ipyleaflet import Map, GeoJSON, LayersControl, CircleMarker


    point1 = Feature(geometry=Point([144.834823, -37.771257]))
    point2 = Feature(geometry=Point([145.14244, -37.830937]))

    m = Map(center=[-37.80415546165204, 145.0286749005318], zoom=11)

    start_geo_json = GeoJSON(name="Start Point", data=point1)
    end_geo_json = GeoJSON(name="End Point", data=point2)
    m.add_layer(start_geo_json)
    m.add_layer(end_geo_json)

    midpoint_coord = midpoint(point1, point2)["geometry"]["coordinates"]
    circle_marker = CircleMarker(name="Midpoint")
    circle_marker.location = (midpoint_coord[1], midpoint_coord[0])
    circle_marker.radius = 10
    circle_marker.color = "red"
    m.add_layer(circle_marker)

    control = LayersControl(position="topright")
    m.add_control(control)

    m


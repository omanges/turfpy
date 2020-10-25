Square
======
Takes a bounding box and calculates the minimum square bounding box that would contain the input.


Example
-------

.. jupyter-execute::

    from turfpy.measurement import square
    bbox = [-20, -20, -15, 0]
    square(bbox)



Interactive Example
-------------------

.. jupyter-execute::

    from turfpy.measurement import square, bbox_polygon
    from geojson import Point, Feature
    from ipyleaflet import Map, GeoJSON, LayersControl

    bbox = [-20, -20, -15, 0]

    sqaure_geo_json = GeoJSON(
        name="Sqaure for the given Bounding Box",
        data=bbox_polygon(square(bbox)),
        style={"color": "red"},
    )
    bbox_polygon_geojson = GeoJSON(name="Bounding Box", data=bbox_polygon(bbox))

    m = Map(center=[-8.484257262005082, -11.58611297607422], zoom=4)

    control = LayersControl(position="topright")
    m.add_control(control)

    m.add_layer(sqaure_geo_json)
    m.add_layer(bbox_polygon_geojson)
    m
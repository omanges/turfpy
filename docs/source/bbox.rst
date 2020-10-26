Bbox
=====
Generate bounding box coordinates for given geojson.

Example
-------

.. jupyter-execute::

    from turfpy.measurement import bbox
    from geojson import Polygon

    p = Polygon([[(2.38, 57.322), (23.194, -20.28), (-120.43, 19.15), (2.38, 57.322)]])
    bbox(p)


Interactive Example
-------------------

.. jupyter-execute::

    from turfpy.measurement import bbox
    from geojson import Polygon
    from geojson import Feature
    from ipyleaflet import Map, GeoJSON, WidgetControl
    from ipywidgets import HTML

    p = Polygon([[(2.38, 57.322), (23.194, -20.28), (-120.43, 19.15), (2.38, 57.322)]])


    geo_json = GeoJSON(data=Feature(geometry=p))

    m = Map(center=[20.04303061200023, -11.832275390625002], zoom=2)

    m.add_layer(geo_json)

    html = HTML()
    html.layout.margin = "0px 20px 10px 20px"
    html.value = """
            <h4>Bounding Box for given geojson</h4>
            <h4>{}</h4>
        """.format(
        bbox(p)
    )
    control = WidgetControl(widget=html, position="topright")
    m.add_control(control)

    m
Polygon to Line
================
Takes a Polygon or MultiPolygon and convert it to a line.

Example
-------

.. jupyter-execute::

    from geojson import Feature, Polygon
    from turfpy.feature_conversion import polygon_to_line

    feature_1 = Feature(geometry=Polygon([[(2.38, 57.322), (23.194, -20.28), (-120.43, 19.15), (2.38, 57.322)]]))
    polygon_to_line(feature_1)

Interactive Example
-------------------

.. jupyter-execute::

    from turfpy.feature_conversion import polygon_to_line
    from geojson import Polygon
    from geojson import Feature
    from ipyleaflet import Map, WidgetControl
    from ipywidgets import HTML

    feature_1 = Feature(geometry=Polygon([[(2.38, 57.322), (23.194, -20.28), (-120.43, 19.15), (2.38, 57.322)]]))

    geo_json = polygon_to_line(feature_1)

    m = Map(center=[20.04303061200023, -11.832275390625002], zoom=2)

    m.add_layer(geo_json)

    html = HTML()
    html.layout.margin = "0px 20px 10px 20px"
    html.value = """
            <h4>Polygon to Line for given geojson</h4>
            <h4>{}</h4>
        """.format(
        geo_json
    )
    control = WidgetControl(widget=html, position="topright")
    m.add_control(control)

    m

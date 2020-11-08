Area
=====
Takes a geojson and measures its length in the specified units.

Example
-------

.. jupyter-execute::

    from turfpy.measurement import length
    from geojson import LineString
    ls = LineString([(115, -32), (131, -22), (143, -25), (150, -34)])
    length(ls)




Interactive Example
-------------------

.. jupyter-execute::

    from turfpy.measurement import length
    from geojson import LineString, Feature
    from ipyleaflet import Map, GeoJSON, WidgetControl
    from ipywidgets import HTML

    ls = LineString([(115, -32), (131, -22), (143, -25), (150, -34)])

    m = Map(center=[-25.52664223616833, 143.44917297363284], zoom=4)

    geo_json = GeoJSON(name="Geojson", data=Feature(geometry=ls))

    m.add_layer(geo_json)

    html = HTML()
    html.layout.margin = "0px 20px 10px 20px"
    html.value = """
            <h4>Length of the given geojson in meters</h4>
            <h4>{}</h4>
        """.format(
        length(ls, units="m")
    )

    control = WidgetControl(widget=html, position="topright")
    m.add_control(control)

    m


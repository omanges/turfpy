Along
=====
This function is used identify a Point at a specified distance along a LineString.

Example
-------

.. jupyter-execute::

    import json
    from turfpy.measurement import along
    from geojson import LineString
    ls = LineString([(-83, 30), (-84, 36), (-78, 41)])
    print(json.dumps(along(ls,200,'mi'), indent=2, sort_keys=True))



Interactive Example
-------------------

.. jupyter-execute::

    from turfpy.measurement import along, length
    from geojson import LineString, Feature
    from ipyleaflet import Map, GeoJSON, WidgetControl, Marker
    from ipywidgets import FloatSlider

    ls = LineString([(-83, 30), (-84, 36), (-78, 41)])


    m = Map(center=[35.47241402319959, -80.11693954467775], zoom=5)
    marker = Marker(location=[30, -83])
    m.add_layer(marker)


    def on_value_change(change):
        global marker
        new_point = along(ls, change["new"], "mi")
        marker.location = new_point["geometry"]["coordinates"][::-1]


    style = {"description_width": "initial"}
    slider = FloatSlider(
        description="Marker position:",
        min=0,
        max=length(ls, units="mi"),
        value=0,
        style=style,
    )
    slider.observe(on_value_change, names="value")

    widget_control1 = WidgetControl(widget=slider, position="topright")
    m.add_control(widget_control1)


    geo_json = GeoJSON(name="Geojson", data=Feature(geometry=ls))

    m.add_layer(geo_json)

    m


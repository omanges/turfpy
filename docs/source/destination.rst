Destination
===========
Takes a Point and calculates the location of a destination point given a distance in degrees, radians, miles, or kilometers and bearing in degrees.


Example
-------

.. jupyter-execute::

    import json
    from turfpy.measurement import destination
    from geojson import Point, Feature

    origin = Feature(geometry=Point([-75.343, 39.984]))
    distance = 50
    bearing = 90
    options = {'units': 'mi'}
    print(json.dumps(destination(origin,distance,bearing,options), indent=2, sort_keys=True))


Interactive Example
-------------------

.. jupyter-execute::

    from turfpy.measurement import destination
    from geojson import Point, Feature
    from ipyleaflet import Map, GeoJSON, WidgetControl, LayersControl, CircleMarker
    from ipywidgets import HTML

    origin = Feature(geometry=Point([-75.343, 39.984]))
    distance = 50
    bearing = 90
    options = {"units": "mi"}

    m = Map(center=[39.98304755619415, -74.67888951301576], zoom=9)


    geo_json = GeoJSON(name="Start Point", data=origin)

    centre_coord = destination(origin, distance, bearing, options)["geometry"][
        "coordinates"
    ]
    circle_marker = CircleMarker(name="End Point")
    circle_marker.location = (centre_coord[1], centre_coord[0])
    circle_marker.radius = 10
    circle_marker.color = "red"


    m.add_layer(geo_json)
    m.add_layer(circle_marker)

    html = HTML()
    html.layout.margin = "0px 20px 10px 20px"
    html.value = """
            <h4>Point which is at 90 degrees bearing and 50 miles in that direction</h4>
        """

    control = WidgetControl(widget=html, position="topright")
    m.add_control(control)

    control = LayersControl(position="topright")
    m.add_control(control)

    m


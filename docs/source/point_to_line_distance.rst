Point To Line Distance
======================
Returns the minimum distance between a Point and any segment of the LineString.


Example
-------

.. jupyter-execute::

    from turfpy.measurement import point_to_line_distance
    from geojson import LineString, Point, Feature
    point = Feature(geometry=Point([0, 0]))
    linestring = Feature(geometry=LineString([(1, 1),(-1, 1)]))
    point_to_line_distance(point, linestring)



Interactive Example
-------------------

.. jupyter-execute::

    from turfpy.measurement import point_to_line_distance
    from geojson import LineString, Point, Feature
    from ipyleaflet import Map, GeoJSON, LayersControl, WidgetControl
    from ipywidgets import HTML

    point = Feature(geometry=Point([0, 0]))
    linestring = Feature(geometry=LineString([(1, 1),(-1, 1)]))

    m = Map(center=[0.5427636983179688, 0.3891992568969727], zoom=8)

    geo_json = GeoJSON(name='Point', data=point)

    m.add_layer(geo_json)

    point_geojson = GeoJSON(name='Linestring', data=linestring)

    m.add_layer(point_geojson)

    html = HTML()
    html.layout.margin = '0px 20px 10px 20px'
    html.value = '''
            <h4>Minimum distance between the Point and the LineString in meters</h4>
            <h4>{}</h4>
        '''.format(point_to_line_distance(point, linestring, units='m'))

    control = WidgetControl(widget=html, position='topright')
    m.add_control(control)

    m


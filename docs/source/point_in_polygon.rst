Point In Polygon
================
Takes a Point or a Point Feature and Polygon or Polygon Feature as input and returns True if Point is in given Feature.


Example
-------

.. jupyter-execute::

    from turfpy.measurement import boolean_point_in_polygon
    from geojson import Point, MultiPolygon, Feature
    point = Feature(geometry=Point([-77, 44]))
    polygon = Feature(geometry=MultiPolygon([([(-81, 41), (-81, 47), (-72, 47), (-72, 41), (-81, 41)],),
    ([(3.78, 9.28), (-130.91, 1.52), (35.12, 72.234), (3.78, 9.28)],)]))
    boolean_point_in_polygon(point, polygon)




Interactive Example
-------------------

.. jupyter-execute::

    from turfpy.measurement import boolean_point_in_polygon
    from geojson import Point, MultiPolygon, Feature
    from ipyleaflet import Map, GeoJSON, LayersControl

    point = Feature(geometry=Point([-77, 44]))
    polygon = Feature(
        geometry=MultiPolygon(
            [
                ([(-81, 41), (-81, 47), (-72, 47), (-72, 41), (-81, 41)],),
                ([(3.78, 9.28), (-130.91, 1.52), (35.12, 72.234), (3.78, 9.28)],),
            ]
        )
    )
    boolean_point_in_polygon(point, polygon)

    m = Map(center=[46.57868671298067, -40.91583251953126], zoom=2)

    geo_json = GeoJSON(name="MultiPolygon Feature", data=polygon)

    m.add_layer(geo_json)

    point_geojson = GeoJSON(name="Point in Polygon", data=point)

    m.add_layer(point_geojson)

    control = LayersControl(position="topright")
    m.add_control(control)

    m



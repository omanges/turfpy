Line Segment
================
Creates a FeatureCollection of 2-vertex LineString segments from a (Multi)LineString or (Multi)Polygon.

Example
-------

.. jupyter-execute::

    from turfpy.misc import line_segment

    poly = {
          "type": "Feature",
          "properties": {},
          "geometry": {
            "type": "Polygon",
            "coordinates": [
              [
                [
                  51.17431640625,
                  47.025206001585396
                ],
                [
                  45.17578125,
                  43.13306116240612
                ],
                [
                  54.5361328125,
                  41.85319643776675
                ],
                [
                  51.17431640625,
                  47.025206001585396
                ]
              ]
            ]
          }
    }

    line_segment(poly)


Interactive Example
-------------------

.. jupyter-execute::

    from ipyleaflet import Map, GeoJSON, LayersControl
    from turfpy.misc import line_segment

    m = Map(center=[44.52337579109473, 50.61581611633301], zoom=6)

    poly = {
          "type": "Feature",
          "properties": {},
          "geometry": {
            "type": "Polygon",
            "coordinates": [
              [
                [
                  51.17431640625,
                  47.025206001585396
                ],
                [
                  45.17578125,
                  43.13306116240612
                ],
                [
                  54.5361328125,
                  41.85319643776675
                ],
                [
                  51.17431640625,
                  47.025206001585396
                ]
              ]
            ]
          }
    }

    polygon = GeoJSON(name="Polygon", data=poly, style={'color':'red'})

    m.add_layer(polygon)

    segments = GeoJSON(name="segments", data=line_segment(poly))
    m.add_layer(segments)

    control = LayersControl(position='topright')
    m.add_control(control)

    m


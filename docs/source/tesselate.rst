Tesselate
================
Tesselates a Feature into a FeatureCollection of triangles using earcut.


Interactive Example
-------------------

.. jupyter-execute::

    from geojson import Feature
    from turfpy.transformation import tesselate

    f = Feature(
        geometry={
            "coordinates": [
                [[11, 0], [22, 4], [31, 0], [31, 11], [21, 15], [11, 11], [11, 0]]
            ],
            "type": "Polygon",
        }
    )

    from ipyleaflet import Map, GeoJSON, LayersControl

    m = Map(center=(4.595931675360621, 29.52129364013672), zoom=4)
    geo_json = GeoJSON(
        name="original",
        data=dict(f),
        style={"opacity": 1, "fillOpacity": 0.3, "weight": 1},
        hover_style={"color": "green", "dashArray": "0", "fillOpacity": 0.5},
    )

    result = tesselate(f)
    m = Map(center=(4.595931675360621, 29.52129364013672), zoom=4)
    geo_json2 = GeoJSON(
        name="tesselate",
        data=result,
        style={"opacity": 1, "fillOpacity": 0.3, "weight": 1},
        hover_style={"color": "green", "dashArray": "0", "fillOpacity": 0.5},
    )
    m.add_layer(geo_json2)
    control = LayersControl(position="topright")
    m.add_control(control)
    m.add_layer(geo_json)
    m
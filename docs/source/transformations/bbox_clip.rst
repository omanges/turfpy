Bbox clip
=========

Takes a Feature or geometry and a bbox and clips the feature to the bbox.

Example
-------

.. jupyter-execute::

    import json
    from turfpy.transformation import bbox_clip
    from geojson import Feature
    f = Feature(geometry={"coordinates": [[[2, 2], [8, 4],
    [12, 8], [3, 7], [2, 2]]], "type": "Polygon"})
    bbox = [0, 0, 10, 10]
    bc = bbox_clip(f, bbox)
    print(json.dumps(bc, indent=2, sort_keys=True))



Interactive Example
-------------------

.. jupyter-execute::

    from geojson import Feature
    from ipyleaflet import Map, GeoJSON, LayersControl
    from turfpy.transformation import bbox_clip, bbox_polygon


    f = Feature(
        geometry={
            "coordinates": [[[2, 2], [8, 4], [12, 8], [3, 7], [2, 2]]],
            "type": "Polygon",
        }
    )

    bbox = [0, 0, 10, 10]

    geo_json = GeoJSON(name="Polygon", data=f)

    bbox_polygon_geojson = GeoJSON(
        name="Bounding Box Polygon", data=bbox_polygon(bbox), style={"color": "green"}
    )

    cliped_geojson = GeoJSON(
        name="Clipped Polygon", data=bbox_clip(f, bbox), style={"color": "red"}
    )


    m = Map(center=[4.889835742990713, 5.82601547241211], zoom=5)

    m.add_layer(geo_json)
    m.add_layer(bbox_polygon_geojson)
    m.add_layer(cliped_geojson)

    control = LayersControl(position="topright")
    m.add_control(control)

    m


Bbox Polygon
============
Generate a Polygon Feature for the bounding box generated using bbox.


Example
-------

.. jupyter-execute::

    import json

    from turfpy.measurement import bbox_polygon, bbox
    from geojson import Polygon

    p = Polygon([[(2.38, 57.322), (23.194, -20.28), (-120.43, 19.15), (2.38, 57.322)]])
    bb = bbox(p)
    print(json.dumps(bbox_polygon(bb), indent=2, sort_keys=True))


Interactive Example
-------------------

.. jupyter-execute::

    from turfpy.measurement import bbox_polygon, bbox
    from geojson import Polygon, Feature
    from ipyleaflet import Map, GeoJSON, WidgetControl, LayersControl

    p = Polygon([[(2.38, 57.322), (23.194, -20.28), (-120.43, 19.15), (2.38, 57.322)]])
    bb = bbox(p)
    geo_json = GeoJSON(name="Geojson", data=Feature(geometry=p))
    bbox_polygon_geojson = GeoJSON(
        name="Bounding Box Polygon", data=bbox_polygon(bb), style={"color": "red"}
    )

    m = Map(center=[20.04303061200023, -11.832275390625002], zoom=2)

    control = LayersControl(position="topright")
    m.add_control(control)

    m.add_layer(geo_json)
    m.add_layer(bbox_polygon_geojson)
    m


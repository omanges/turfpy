Random Position
================

Generates a random position, if bbox provided then the generated position will be in the bbox.

Example
-------

.. jupyter-execute::

    from turfpy.random import random_position

    random_position(bbox=[11.953125, 18.979025953255267, 52.03125, 46.558860303117164])


Interactive Example
-------------------

.. jupyter-execute::

    from geojson import Feature
    from ipyleaflet import Map, GeoJSON
    from turfpy.random import random_position
    from turfpy.measurement import bbox_polygon

    bb = [11.953125, 18.979025953255267, 52.03125, 46.558860303117164]

    random_pos = random_position(bbox=bb)

    f = Feature(
        geometry={
            "coordinates": random_pos,
            "type": "Point",
        }
    )

    geo_json = GeoJSON(name="Position", data=f)



    bbox_polygon_geojson = GeoJSON(
            name="Bounding Box Polygon", data=bbox_polygon(bb), style={"color": "red"}
        )


    m = Map(center=[4.889835742990713, 5.82601547241211], zoom=1)

    m.add_layer(geo_json)
    m.add_layer(bbox_polygon_geojson)

    m
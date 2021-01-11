Random Points
==============

Generates geojson random points, if bbox provided then the generated points will be in the bbox.

Example
-------

.. jupyter-execute::

    from turfpy.random import random_points

    random_points(count=3, bbox=[11.953125, 18.979025953255267, 52.03125, 46.558860303117164])


Interactive Example
-------------------

.. jupyter-execute::

    from geojson import Feature
    from ipyleaflet import Map, GeoJSON
    from turfpy.random import random_points
    from turfpy.measurement import bbox_polygon

    bb = [11.953125, 18.979025953255267, 52.03125, 46.558860303117164]

    fc = random_points(count=3, bbox=[11.953125, 18.979025953255267, 52.03125, 46.558860303117164])

    geo_json = GeoJSON(name="Points", data=fc)



    bbox_polygon_geojson = GeoJSON(
            name="Bounding Box Polygon", data=bbox_polygon(bb), style={"color": "red"}
        )


    m = Map(center=[4.889835742990713, 5.82601547241211], zoom=1)

    m.add_layer(geo_json)
    m.add_layer(bbox_polygon_geojson)

    m
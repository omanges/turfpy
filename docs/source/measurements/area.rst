Area
=====
Calculates the area of the input GeoJSON object.

Example
-------

.. jupyter-execute::

    from turfpy.measurement import area
    from geojson import Feature, FeatureCollection

    geometry_1 = {
        "coordinates": [[[0, 0], [0, 10], [10, 10], [10, 0], [0, 0]]],
        "type": "Polygon",
    }
    geometry_2 = {
        "coordinates": [
            [[2.38, 57.322], [23.194, -20.28], [-120.43, 19.15], [2.38, 57.322]]
        ],
        "type": "Polygon",
    }
    feature_1 = Feature(geometry=geometry_1)
    feature_2 = Feature(geometry=geometry_2)
    feature_collection = FeatureCollection([feature_1, feature_2])

    area(feature_collection)


Interactive Example
-------------------

.. jupyter-execute::

    from turfpy.measurement import area
    from geojson import Feature, FeatureCollection
    from ipyleaflet import Map, GeoJSON, basemaps, basemap_to_tiles, WidgetControl
    from ipywidgets import HTML

    geometry_1 = {
        "coordinates": [[[0, 0], [0, 10], [10, 10], [10, 0], [0, 0]]],
        "type": "Polygon",
    }
    geometry_2 = {
        "coordinates": [
            [[2.38, 57.322], [23.194, -20.28], [-120.43, 19.15], [2.38, 57.322]]
        ],
        "type": "Polygon",
    }
    feature_1 = Feature(geometry=geometry_1)
    feature_2 = Feature(geometry=geometry_2)
    feature_collection = FeatureCollection([feature_1, feature_2])
    geo_json = GeoJSON(data=feature_collection)
    mapnik = basemap_to_tiles(basemaps.OpenStreetMap.Mapnik)

    m = Map(layers=(mapnik,), center=[20.04303061200023, -11.832275390625002], zoom=2)

    m.add_layer(geo_json)

    html = HTML()
    html.layout.margin = "0px 20px 10px 20px"
    html.value = """
            <h4>Area in meter sqaure: {}</h4>
            <h4>measurement.area(feature_collection)</h4>
        """.format(
        area(feature_collection)
    )
    control = WidgetControl(widget=html, position="topright")
    m.add_control(control)
    m

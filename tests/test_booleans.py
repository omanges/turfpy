"""
This module will test all functions in booleans module.
"""

from turfpy.booleans import (
    boolean_within
)

def test_boolean_within():
    """Test boolean_within function."""

    point = {
      "type": "Feature",
      "properties": {},
      "geometry": {
        "coordinates": [
          -104.99089477656028,
          39.74071889567193
        ],
        "type": "Point"
      }
    }
    polygon = {
      "type": "Feature",
      "properties": {},
      "geometry": {
        "coordinates": [
          [
            [
              -105.50078324787434,
              39.94526320322274
            ],
            [
              -105.50078324787434,
              39.49578832519356
            ],
            [
              -104.31486287077342,
              39.49578832519356
            ],
            [
              -104.31486287077342,
              39.94526320322274
            ],
            [
              -105.50078324787434,
              39.94526320322274
            ]
          ]
        ],
        "type": "Polygon"
      }
    }
    polygon2 = {
      "type": "Feature",
      "properties": {},
      "geometry": {
        "coordinates": [
          [
            [
              -105.08511409757845,
              39.77709223878705
            ],
            [
              -105.08511409757845,
              39.64746354274314
            ],
            [
              -104.85762505063519,
              39.64746354274314
            ],
            [
              -104.85762505063519,
              39.77709223878705
            ],
            [
              -105.08511409757845,
              39.77709223878705
            ]
          ]
        ],
        "type": "Polygon"
      }
    }
    polygon3 = {
      "type": "Feature",
      "properties": {},
      "geometry": {
        "coordinates": [
          [
            [
              -107.1914941618692,
              40.48568881564137
            ],
            [
              -107.1914941618692,
              40.41195426635508
            ],
            [
              -107.02719651685456,
              40.41195426635508
            ],
            [
              -107.02719651685456,
              40.48568881564137
            ],
            [
              -107.1914941618692,
              40.48568881564137
            ]
          ]
        ],
        "type": "Polygon"
      }
    }
    polygon4 = {
      "type": "Feature",
      "properties": {},
      "geometry": {
        "type": "Polygon",
        "coordinates": [
          [
            [1, 1],
            [1, 10],
            [10, 10],
            [10, 1],
            [1, 1]
          ]
        ]
      }
    }
    point2 = {
      "type": "Feature",
      "properties": {},
      "geometry": {
        "coordinates": [
          -114.99089477656028,
          39.74071889567193
        ],
        "type": "Point"
      }
    }
    multi_point = {
      "type": "Feature",
      "properties": {},
      "geometry": {
        "coordinates": [
          [
            -104.99089477656028,
            39.74071889567193
          ]
        ],
        "type": "MultiPoint"
      }
    }
    multi_point2 = {
      "type": "Feature",
      "properties": {},
      "geometry": {
        "coordinates": [
          [
            -114.99089477656028,
            39.74071889567193
          ]
        ],
        "type": "MultiPoint"
      }
    }
    multi_point3 = {
      "type": "Feature",
      "properties": {},
      "geometry": {
        "coordinates": [
          [
            -104.94503973465616,
            39.68884174056387
          ]
        ],
        "type": "MultiPoint"
      }
    }
    line1 = {
      "type": "Feature",
      "properties": {},
      "geometry": {
        "coordinates": [
          [
            -105.02495945404148,
            39.69616279727023
          ],
          [
            -104.94503973465616,
            39.68884174056387
          ]
        ],
        "type": "LineString"
      }
    }
    line2 = {
      "type": "Feature",
      "properties": {},
      "geometry": {
        "coordinates": [
          [
            -106.16666973097443,
            39.28793457983201
          ],
          [
            -106.03537304912723,
            39.2658397561942
          ]
        ],
        "type": "LineString"
      }
    }
    line3 = {
      "type": "Feature",
      "properties": {},
      "geometry": {
        "type": "LineString",
        "coordinates": [
          [1, 2],
          [1, 3],
          [1, 15.5]
        ]
      }
    }
    line4 = {
      "type": "Feature",
      "properties": {},
      "geometry": {
        "type": "LineString",
        "coordinates": [
          [1, 2],
          [1, 3],
          [1, 3.5]
        ]
      }
    }
    


    point_in_poly_true = boolean_within(point, polygon)
    assert point_in_poly_true == True

    point_in_poly_false = boolean_within(point2, polygon)
    assert point_in_poly_false == False

    multi_point_in_poly_true = boolean_within(multi_point, polygon)
    assert multi_point_in_poly_true == True

    multi_point_in_poly_false = boolean_within(multi_point2, polygon)
    assert multi_point_in_poly_false == False

    multi_point_in_multi_point_true = boolean_within(multi_point, multi_point)
    assert multi_point_in_multi_point_true == True

    multi_point_in_multi_point_false = boolean_within(multi_point, multi_point2)
    assert multi_point_in_multi_point_false == False

    point_in_multi_point_true = boolean_within(point, multi_point)
    assert point_in_multi_point_true == True

    point_in_multi_point_false = boolean_within(point, multi_point2)
    assert point_in_multi_point_false == False

    polygon_in_polygon_true = boolean_within(polygon2, polygon)
    assert polygon_in_polygon_true == True

    polygon_in_polygon_false = boolean_within(polygon3, polygon)
    assert polygon_in_polygon_false == False

    line_in_polygon_true = boolean_within(line1, polygon)
    assert line_in_polygon_true == True

    line_in_polygon_false = boolean_within(line2, polygon)
    assert line_in_polygon_false == False

    line_in_polygon2_false = boolean_within(line3, polygon4)
    assert line_in_polygon2_false == False

    line_in_polygon3_false = boolean_within(line3, polygon4)
    assert line_in_polygon3_false == False

    multi_point_on_line_true = boolean_within(multi_point3, line1)
    assert multi_point_on_line_true == True
    
    multi_point_on_line_false = boolean_within(multi_point, line1)
    assert multi_point_on_line_false == False

    line_on_line_true = boolean_within(line1, line1)
    assert line_on_line_true == True

    line_on_line_false = boolean_within(line1, line2)
    assert line_on_line_false == False
    
## Misc Examples :
  * Line Intersect : Takes any LineString or Polygon GeoJSON and returns the intersecting point(s).
  
| Argument  | Type | Description |
| ------- | ------ | ----------- |
| `feature1`  | Feature  | Any LineString or Polygon, if one of the two features is polygon to improve performance please pass polygon as this parameter |
| `feature2`  | Feature | Any LineString or Polygon. |

| Return  | Type | Description |
| ------- | ------ | ----------- |
| `points`  | FeatureCollection  | FeatureCollection of intersecting points |

```python
from geojson import LineString, Feature
from turfpy.misc import line_intersect
l1 = Feature(geometry=LineString([[126, -11], [129, -21]]))
l2 = Feature(geometry=LineString([[123, -18], [131, -14]]))
line_intersect(l1, l2)
```

  * Line Segment : Creates a FeatureCollection of 2-vertex LineString segments from a (Multi)LineString or (Multi)Polygon.

| Argument  | Type | Description |
| ------- | ------ | ----------- |
| `geojson`  | Geometry or Feature or FeatureCollection  | GeoJSON Polygon or LineString |

| Return  | Type | Description |
| ------- | ------ | ----------- |
| `segments`  | FeatureCollection  | FeatureCollection 2-vertex line segments |

```python
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
```

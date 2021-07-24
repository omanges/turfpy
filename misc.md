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

  * Line Arc : Creates a circular arc, of a circle of the given radius and center point,
    between bearing1 and bearing2; 0 bearing is
    North of center point, positive clockwise.

| Argument  | Type | Description |
| ------- | ------ | ----------- |
| `center`  | Feature   | A `Point` object representing center point of circle |
| `radius`  | float  | An int representing radius of the circle |
| `bearing1`  | float  | Angle, in decimal degrees, of the first radius of the arc |
| `bearing2`  | float  | Angle, in decimal degrees, of the second radius of the arc |
| `options`  | float  | A dict representing additional properties,which can be `steps` which has default values as 64 and `units` which has default values of `km` |

| Return  | Type | Description |
| ------- | ------ | ----------- |
| `line string`  | Feature  | A Line String feature object. |

```python
from turfpy.misc import line_arc
from geojson import Feature, Point

center = Feature(geometry=Point((-75, 40)))
radius = 5
bearing1 = 25
bearing2 = 47

line_arc(center=center, radius=radius, bearing1=bearing1, bearing2=bearing2)
```


  * Line Arc : Creates a circular sector of a circle of given radius and center Point ,
    between (clockwise) bearing1 and bearing2; 0
    bearing is North of center point, positive clockwise.

| Argument  | Type | Description |
| ------- | ------ | ----------- |
| `center`  | Feature   | A `Point` object representing center point of circle |
| `radius`  | float  | An int representing radius of the circle |
| `bearing1`  | float  | Angle, in decimal degrees, of the first radius of the arc |
| `bearing2`  | float  | Angle, in decimal degrees, of the second radius of the arc |
| `options`  | float  | A dict representing additional properties, which can be `steps` which has default values as 64, `units` which has default values of `km`, and `properties` which will be added to resulting Feature as properties. |

| Return  | Type | Description |
| ------- | ------ | ----------- |
| `polygon`  | Feature  | A polygon feature object. |

```python
from turfpy.misc import sector
from geojson import Feature, Point

center = Feature(geometry=Point((-75, 40)))
radius = 5
bearing1 = 25
bearing2 = 45

feature = sector(center, radius, bearing1, bearing2, options={"properties":{"length":3}})
```
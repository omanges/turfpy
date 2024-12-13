## Measurement Examples :
  * Bearing : Takes two Point and finds the geographic bearing between them.
  
| Argument  | Type | Description |
| ------- | ------ | ----------- |
| `start`  | Feature  | Start point |
| `end`  | Feature | Ending point |
| `final`  | Boolean(Optional) | Calculates the final bearing if true |

| Return  | Type | Description |
| ------- | ------ | ----------- |
| `bearing`  | float  | Calculates bearing|

```python
from turfpy import measurement
from geojson import Point, Feature
start = Feature(geometry=Point((-75.343, 39.984)))
end = Feature(geometry=Point((-75.534, 39.123)))
measurement.bearing(start,end)
```

* Distance : Calculates distance between two Points. A point is containing latitude and logitude in decimal degrees and ``unit`` is optional.

| Argument  | Type | Description |
| ------- | ------ | ----------- |
| `point1`  | Feature  | Start point |
| `point2`  | Feature | Ending point |
| `units`  | str(Optional) | A string containing unit, default is 'km' refer [Units type](#units-type) section |

| Return  | Type | Description |
| ------- | ------ | ----------- |
| `distance`  | float  | The distance between the two points in the requested unit |

```python
from turfpy import measurement
from geojson import Point, Feature
start = Feature(geometry=Point((-75.343, 39.984)))
end = Feature(geometry=Point((-75.534, 39.123)))
measurement.distance(start,end)
```

* Area : This function calculates the area of the Geojson object given as input.

| Argument  | Type | Description |
| ------- | ------ | ----------- |
| `geojson`  | Any Geojson Type | Geojson object for which area is to be found |

| Return  | Type | Description |
| ------- | ------ | ----------- |
| `area`  | float  | Area for the given Geojson object in square meters |

```python
from turfpy.measurement import area
from geojson import Feature, FeatureCollection

geometry_1 = {"coordinates": [[[0, 0], [0, 10], [10, 10], [10, 0], [0, 0]]], "type": "Polygon"};
geometry_2 = {"coordinates": [[[2.38, 57.322], [23.194, -20.28], [-120.43, 19.15], [2.38, 57.322]]], "type": "Polygon"};
feature_1 = Feature(geometry=geometry_1)
feature_2 = Feature(geometry=geometry_2)
feature_collection = FeatureCollection([feature_1, feature_2])

area(feature_collection)
```


* Bbox : This function is used to generate bounding box coordinates for given geojson.

| Argument  | Type | Description |
| ------- | ------ | ----------- |
| `geojson`  | Any Geojson Type  | Geojson object for which bounding box is to be found |

| Return  | Type | Description |
| ------- | ------ | ----------- |
| `bbox`  | list  | Bounding box points for the given Geojson object |

```python
from turfpy.measurement import bbox
from geojson import Polygon

p = Polygon([[(2.38, 57.322), (23.194, -20.28), (-120.43, 19.15), (2.38, 57.322)]])
bb = bbox(p)
```

* Bbox Polygon : To generate a Polygon Feature for the bounding box generated using bbox.

| Argument  | Type | Description |
| ------- | ------ | ----------- |
| `bbox`  | list  | Bounding box generated for a geojson |
| `properties`  | dict(Optional) | Properties to be added to the returned feature |

| Return  | Type | Description |
| ------- | ------ | ----------- |
| `bbox_polygon`  | Polygon  | Polygon for the given bounding box coordinates |

```python
from turfpy.measurement import bbox_polygon, bbox
from geojson import Polygon

p = Polygon([[(2.38, 57.322), (23.194, -20.28), (-120.43, 19.15), (2.38, 57.322)]])
bb = bbox(p)
feature = bbox_polygon(bb)
```

* Center : Takes a Feature or FeatureCollection and returns the absolute center point of all features.

| Argument  | Type | Description |
| ------- | ------ | ----------- |
| `geojson`  | Any Geojson Type  | GeoJSON for which centered to be calculated |
| `properties`  | dict(Optional) | Properties to be added to the returned feature |

| Return  | Type | Description |
| ------- | ------ | ----------- |
| `center`  | Feature  | Point feature for the center |

```python
from turfpy.measurement import center
from geojson import Feature, FeatureCollection, Point

f1 = Feature(geometry=Point((-97.522259, 35.4691)))
f2 = Feature(geometry=Point((-97.502754, 35.463455)))
f3 = Feature(geometry=Point((-97.508269, 35.463245)))
feature_collection = FeatureCollection([f1, f2, f3])
feature = center(feature_collection)
```

* Envelope : Takes any number of features and returns a rectangular Polygon that encompasses all vertices.

| Argument  | Type | Description |
| ------- | ------ | ----------- |
| `geojson`  | Any Geojson Type  | Geojson object for which envelope is to be found |

| Return  | Type | Description |
| ------- | ------ | ----------- |
| `bbox`  | Polygon  | Returns envelope i.e bounding box polygon |

```python
from turfpy.measurement import envelope
from geojson import Feature, FeatureCollection, Point

f1 = Feature(geometry=Point((-97.522259, 35.4691)))
f2 = Feature(geometry=Point((-97.502754, 35.463455)))
f3 = Feature(geometry=Point((-97.508269, 35.463245)))
feature_collection = FeatureCollection([f1, f2, f3])
feature = envelope(feature_collection)
```

* Length : Takes a geojson and measures its length in the specified units.

| Argument  | Type | Description |
| ------- | ------ | ----------- |
| `geojson`  | Any Geojson Type  | Geojson for which the length is to be determined |
| `units`  | str(Optional) | Properties to be added to the returned feature, default is 'km' refer [Units type](#units-type) section  |

| Return  | Type | Description |
| ------- | ------ | ----------- |
| `length`  | float  | Length of the geojson in specified units |

```python
from turfpy.measurement import length
from geojson import LineString
ls = LineString([(115, -32), (131, -22), (143, -25), (150, -34)])
length(ls)
```

* Destination : Takes a Point and calculates the location of a destination point given a distance in degrees, radians, miles, or kilometers and bearing in degrees.

| Argument  | Type | Description |
| ------- | ------ | ----------- |
| `origin`  | Feature  | Start point |
| `distance`  | float | distance upto which the destination is from origin |
| `bearing`  | bearing  | Direction in which is the destination is from origin |
| `options`  | dict(Optional) | Option like units of distance and properties to be passed to destination point feature, default is 'km' refer [Units type](#units-type) section, example {'units':'mi', 'properties': {"marker-color": "F00"} |

| Return  | Type | Description |
| ------- | ------ | ----------- |
| `Destination`  | Feature  | Destination point in at the given distance and given direction |

```python
from turfpy.measurement import destination
from geojson import Point, Feature
origin = Feature(geometry=Point([-75.343, 39.984]))
distance = 50
bearing = 90
options = {'units': 'mi'}
destination(origin,distance,bearing,options)
```

* Centroid : Takes one or more features and calculates the centroid using the mean of all vertices.

| Argument  | Type | Description |
| ------- | ------ | ----------- |
| `geojson`  | Any Geojson Type  | Input features |
| `properties`  | dict(Optional) | Properties to be added to the returned feature |

| Return  | Type | Description |
| ------- | ------ | ----------- |
| `centroid`  | Feature  | Point feature which is the centroid of the given features |

```python
from turfpy.measurement import centroid
from geojson import Polygon
polygon = Polygon([[(-81, 41), (-88, 36), (-84, 31), (-80, 33), (-77, 39), (-81, 41)]])
centroid(polygon)
```

* Along : This function is used identify a Point at a specified distance along a LineString.

| Argument  | Type | Description |
| ------- | ------ | ----------- |
| `line`  | Feature  | LineString on which the point to be identified |
| `dist`  | dict(Optional) | Distance from the start of the LineString |
| `unit`  | str(Optional) | Unit of distance, default is 'km' refer [Units type](#units-type) section |

| Return  | Type | Description |
| ------- | ------ | ----------- |
| `point`  | Feature  | Point at the distance on the LineString passed |

```python
from turfpy.measurement import along
from geojson import LineString
ls = LineString([(-83, 30), (-84, 36), (-78, 41)])
along(ls,200,'mi')
```

* Midpoint : This function is used to get midpoint between any the two points.

| Argument  | Type | Description |
| ------- | ------ | ----------- |
| `point1`  | Feature  | First point |
| `point2`  | Feature | Second Point |

| Return  | Type | Description |
| ------- | ------ | ----------- |
| `point`  | Feature  | Point which is the midpoint of the two points given as input |

```python
from turfpy.measurement import midpoint
from geojson import Point, Feature
point1 = Feature(geometry=Point([144.834823, -37.771257]))
point2 = Feature(geometry=Point([145.14244, -37.830937]))
midpoint(point1, point2)
```

* Nearest Point : Takes a reference Point Feature and FeatureCollection of point features and returns the point from the FeatureCollection closest to the reference Point Feature.

| Argument  | Type | Description |
| ------- | ------ | ----------- |
| `target_point`  | Feature  | Feature Point of reference |
| `points`  | FeatureCollection | FeatureCollection of points |

| Return  | Type | Description |
| ------- | ------ | ----------- |
| `point`  | Feature  | Point Feature from the FeatureCollection which is closest to the reference Point |

```python
from turfpy.measurement import nearest_point
from geojson import Point, Feature, FeatureCollection
f1 = Feature(geometry=Point([28.96991729736328,41.01190001748873]))
f2 = Feature(geometry=Point([28.948459, 41.024204]))
f3 = Feature(geometry=Point([28.938674, 41.013324]))
fc = FeatureCollection([f1, f2 ,f3])
t = Feature(geometry=Point([28.973865, 41.011122]))
nearest_point(t ,fc)
```

* Point On Feature : Takes a Feature or FeatureCollection and returns a Point guaranteed to be on the surface of the feature.

| Argument  | Type | Description |
| ------- | ------ | ----------- |
| `geojson`  | Feature or FeatureCollection | Feature or FeatureCollection on which the Point is to be found |

| Return  | Type | Description |
| ------- | ------ | ----------- |
| `point`  | Feature  | Feature point which on the provided feature |

```python
from turfpy.measurement import point_on_feature
from geojson import  Polygon, Feature
point = Polygon([[(116, -36), (131, -32), (146, -43), (155, -25), (133, -9), (111, -22), (116, -36)]])
feature = Feature(geometry=point)
point_on_feature(feature)
```

* Tangent To Polygon : Finds the tangents of a (Multi)Polygon from a Point.

| Argument  | Type | Description |
| ------- | ------ | ----------- |
| `point`  | Feature  | Point or Point Feature |
| `polygon`  | Polygon | (Multi)Polygon or (Multi)Polygon Feature |

| Return  | Type | Description |
| ------- | ------ | ----------- |
| `points`  | FeatureCollection  | FeatureCollection of two tangent Point Feature |

```python
from turfpy.measurement import polygon_tangents
from geojson import Polygon, Point, Feature
point = Feature(geometry=Point([61, 5]))
polygon = Feature(geometry=Polygon([[(11, 0), (22, 4), (31, 0), (31, 11), (21, 15), (11, 11), (11, 0)]]))
polygon_tangents(point, polygon)
```

* Point To Line Distance : Returns the minimum distance between a Point and any segment of the LineString.

| Argument  | Type | Description |
| ------- | ------ | ----------- |
| `point`  | Point or Feature  | Point or Point Feature |
| `line`  | LineString or Feature | (Multi)Polygon or (Multi)Polygon Feature |
| `units`  | str(Optional) | Unit of distance, default is 'km' refer [Units type](#units-type) section |
| `method`  | str(Optional) | Method to calculate distance, value can be `geodesic` or `planar`, default value is geodesic |

| Return  | Type | Description |
| ------- | ------ | ----------- |
| `distance`  | fload  | Approximate distance between the LineString and Point |

```python
from turfpy.measurement import point_to_line_distance
from geojson import LineString, Point, Feature
point = Feature(geometry=Point([0, 0]))
linestring = Feature(geometry=LineString([(1, 1),(-1, 1)]))
point_to_line_distance(point, linestring)
```

* Rhumb Bearing : Takes two points and finds the bearing angle between them along a Rhumb line i.e. the angle measured in degrees start the north line (0 degrees).

| Argument  | Type | Description |
| ------- | ------ | ----------- |
| `start`  | Point or Feature  | Start Point or Point Feature |
| `end`  | Point or Feature  | End Point or Point Feature |
| `final`  | boolean(Optional) | Calculates the final bearing if True, default value is False |

| Return  | Type | Description |
| ------- | ------ | ----------- |
| `bearing`  | fload  | Bearing from north in decimal degrees, between -180 and 180 degrees (positive clockwise) |

```python
from turfpy.measurement import rhumb_bearing
from geojson import Feature, Point
start = Feature(geometry=Point([-75.343, 39.984]))
end = Feature(geometry=Point([-75.534, 39.123]))
rhumb_bearing(start, end, True)
```

* Rhumb Destination : Returns the destination Point having travelled the given distance along a Rhumb line from the origin Point with the (varant) given bearing.

| Argument  | Type | Description |
| ------- | ------ | ----------- |
| `origin`  | Point or Feature  | Start Point or Point Feature |
| `distance`  | float | Distance upto which the destination is from origin |
| `bearing`  | bearing  | Varant bearing angle ranging from -180 to 180 degrees from north |
| `options`  | dict(Optional) | Option like units of distance and properties to be passed to destination point feature, default is 'km' refer [Units type](#units-type) section, example {'units':'mi', 'properties': {"marker-color": "F00"} |

| Return  | Type | Description |
| ------- | ------ | ----------- |
| `Destination`  | Feature  | Destination point in at the given distance and given direction |

```python
from turfpy.measurement import rhumb_destination
from geojson import Point, Feature
start = Feature(geometry=Point([-75.343, 39.984]), properties={"marker-color": "F00"})
distance = 50
bearing = 90
rhumb_destination(start, distance, bearing, {'units':'mi', 'properties': {"marker-color": "F00"}})
```

* Rhumb Distance : Calculates the distance along a rhumb line between two points in degrees, radians, miles, or kilometers.

| Argument  | Type | Description |
| ------- | ------ | ----------- |
| `start`  | Point or Feature  | Start Point or Point Feature from which distance to be calculated |
| `to`  | float | End Point or Point Feature upto which distance to be calculated |
| `units`  | str(Optional) | Unit of distance, default is 'km' refer [Units type](#units-type) section |

| Return  | Type | Description |
| ------- | ------ | ----------- |
| `Destination`  | Feature  | Destination point in at the given distance and given direction |

```python
from turfpy.measurement import rhumb_distance
from geojson import Point, Feature
start = Feature(geometry=Point([-75.343, 39.984]))
end = Feature(geometry=Point([-75.534, 39.123]))
rhumb_distance(start, end,'mi')
```

* Square : Takes a bounding box and calculates the minimum square bounding box that would contain the input.

| Argument  | Type | Description |
| ------- | ------ | ----------- |
| `bbox`  | list  | Bounding box extent in west, south, east, north order |

| Return  | Type | Description |
| ------- | ------ | ----------- |
| `Destination`  | list  | A square surrounding bbox |

```python
from turfpy.measurement import square
bbox = [-20, -20, -15, 0]
square(bbox)
```


## Units Type
Some functionalities support `units` as a parameter, default values of `units` is `kilometers` for the functionalities that have units are parameters. The values for it are:
```text
'km' = kilometers
'm' = meters
'mi = miles
'ft' = feets
'in' = inches
'deg' = degrees
'cen' = centimeters
'rad' = radians
'naut' = nauticals
'yd' = yards
```
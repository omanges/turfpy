## Transformation Examples :
* Circle : Takes a Point and calculates the circle polygon given a radius in degrees, radians, miles, or kilometers; and steps for precision.

| Argument| Type | Description|
| -------   |------ | ----------- |
| `Center`  |Feature  | Center Point |
| `radius`  |Int    | radius of the circle |
| `steps`   |Int    | Number of steps |
| `units`   |str(optional) | Unit of distance, default is 'km' refer [Units type](#units-type) section |
| `kwargs`  |dict(optional) | optional properties |

| Return  | Type | Description |
| ------- | ------ | ----------- |
| `Feature`  | Feature  | A circle polygon |

```python
from turfpy.transformation import circle
from geojson import Point, Feature
circle(center=Feature(geometry=Point((-75.343, 39.984))), radius=5, steps=10)
```

* bbox_clip : Takes a Feature or geometry and a bbox and clips the feature to the bbox.

| Argument| Type | Description|
| -------   |------ | ----------- |
| `geojson`  |Feature  | Geojson data |
| `bbox`  |List    | Bounding Box which is used to clip the geojson |

| Return  | Type | Description |
| ------- | ------ | ----------- |
| `bb_clip`  | Feature  | Clipped geojson |

```python
from turfpy.transformation import bbox_clip
from geojson import Feature
f = Feature(geometry={"coordinates": [[[2, 2], [8, 4],
[12, 8], [3, 7], [2, 2]]], "type": "Polygon"})
bbox = [0, 0, 10, 10]
clip = bbox_clip(f, bbox)
```

* bezie_spline : Takes a line and returns a curved version by applying a Bezier spline algorithm.

| Argument| Type | Description|
| -------   |------ | ----------- |
| `line`  |Feature  | LineString Feature which is used to draw the curve |
| `resolution`  |Float    | Time in milliseconds between points |
| `sharpness`  |Float    | A measure of how curvy the path should be between splines |

| Return  | Type | Description |
| ------- | ------ | ----------- |
| `Curve`  | Feature  | Curve as LineString Feature |

```python
from geojson import LineString, Feature
from turfpy.transformation import bezie_spline
ls = LineString([(-76.091308, 18.427501),
                    (-76.695556, 18.729501),
                    (-76.552734, 19.40443),
                    (-74.61914, 19.134789),
                    (-73.652343, 20.07657),
                    (-73.157958, 20.210656)])
f = Feature(geometry=ls)
bezie_spline(f)
```

* concave : Generate concave hull for the given feature or Feature Collection.

| Argument| Type | Description|
| -------   |------ | ----------- |
| `features`  |Feature or FeatureCollection  | It can be a feature or Feature Collection |
| `alpha`  | Float    | Alpha determines the shape of concave hull, greater values will make shape more tighten. |

| Return  | Type | Description |
| ------- | ------ | ----------- |
| `concave hull`  | Feature  | Feature of concave hull polygon |

```python
from turfpy.transformation import concave
from geojson import FeatureCollection, Feature, Point
f1 = Feature(geometry=Point((-63.601226, 44.642643)))
f2 = Feature(geometry=Point((-63.591442, 44.651436)))
f3 = Feature(geometry=Point((-63.580799, 44.648749)))
f4 = Feature(geometry=Point((-63.573589, 44.641788)))
f5 = Feature(geometry=Point((-63.587665, 44.64533)))
f6 = Feature(geometry=Point((-63.595218, 44.64765)))
fc = [f1, f2, f3, f4, f5, f6]
concave(FeatureCollection(fc), alpha=100)
```

* convex : Generate convex hull for the given feature or Feature Collection.

| Argument| Type | Description|
| -------   |------ | ----------- |
| `features`  |Feature or FeatureCollection  | It can be a feature or Feature Collection |

| Return  | Type | Description |
| ------- | ------ | ----------- |
| `convex hull`  | Feature  | Feature of convex hull polygon |

```python
from turfpy.transformation import convex
from geojson import FeatureCollection, Feature, Point
f1 = Feature(geometry=Point((10.195312, 43.755225)))
f2 = Feature(geometry=Point((10.404052, 43.8424511)))
f3 = Feature(geometry=Point((10.579833, 43.659924)))
f4 = Feature(geometry=Point((10.360107, 43.516688)))
f5 = Feature(geometry=Point((10.14038, 43.588348)))
f6 = Feature(geometry=Point((10.195312, 43.755225)))
fc = [f1, f2, f3, f4, f5, f6]
convex(FeatureCollection(fc))
```

* intersect : Takes polygons and finds their intersection.

| Argument| Type | Description|
| -------   |------ | ----------- |
| `features`  |List[Feature] or FeatureCollection   | List of features of Feature Collection |

| Return  | Type | Description |
| ------- | ------ | ----------- |
| `intersection`  | Feature  | Intersection Geojson Feature |

```python
from turfpy.transformation import intersect
from geojson import Feature
f = Feature(geometry={"coordinates": [
[[-122.801742, 45.48565], [-122.801742, 45.60491],
[-122.584762, 45.60491], [-122.584762, 45.48565],
[-122.801742, 45.48565]]], "type": "Polygon"})
b = Feature(geometry={"coordinates": [
[[-122.520217, 45.535693], [-122.64038, 45.553967],
[-122.720031, 45.526554], [-122.669906, 45.507309],
[-122.723464, 45.446643], [-122.532577, 45.408574],
[-122.487258, 45.477466], [-122.520217, 45.535693]
]], "type": "Polygon"})
inter = intersect([f, b])
```

* union : Given list of features or FeatureCollection return union of those.

| Argument| Type | Description|
| -------   |------ | ----------- |
| `features`  |List[Feature] or FeatureCollection   | A list of GeoJSON features or FeatureCollection. |

| Return  | Type | Description |
| ------- | ------ | ----------- |
| `union`  | Feature  | A GeoJSON Feature or FeatureCollection |

```python
from turfpy.transformation import union
from geojson import Feature, Polygon, FeatureCollection
f1 = Feature(geometry=Polygon([[
    [-82.574787, 35.594087],
    [-82.574787, 35.615581],
    [-82.545261, 35.615581],
    [-82.545261, 35.594087],
     [-82.574787, 35.594087]
]]), properties={"fill": "#00f"})
f2 = Feature(geometry=Polygon([[
    [-82.560024, 35.585153],
    [-82.560024, 35.602602],
    [-82.52964, 35.602602],
    [-82.52964, 35.585153],
    [-82.560024, 35.585153]]]), properties={"fill": "#00f"})
union(FeatureCollection([f1, f2], properties={"combine": "yes"}))
```

* dissolve : Take FeatureCollection or list of features to dissolve based on property_name provided.

| Argument| Type | Description|
| -------   |------ | ----------- |
| `features`  |List[Feature], FeatureCollection  | A list of GeoJSON features or FeatureCollection. |
| `property_name`  |str    | Name of property based on which to dissolve. |

| Return  | Type | Description |
| ------- | ------ | ----------- |
| `dissolved`  | Feature or FeatureCollection  | A GeoJSON Feature or FeatureCollection. |

```python
from geojson import Polygon, Feature, FeatureCollection
from turfpy.transformation import dissolve
f1 = Feature(geometry=Polygon([[
    [0, 0],
    [0, 1],
    [1, 1],
    [1, 0],
    [0, 0]]]), properties={"combine": "yes", "fill": "#00f"})
f2 = Feature(geometry=Polygon([[
    [0, -1],
    [0, 0],
    [1, 0],
    [1, -1],
    [0,-1]]]), properties={"combine": "yes"})
f3 = Feature(geometry=Polygon([[
    [1,-1],
    [1, 0],
    [2, 0],
    [2, -1],
    [1, -1]]]), properties={"combine": "no"})
dissolve(FeatureCollection([f1, f2, f3]), property_name='combine')
```

* difference : Find the difference between given two features.

| Argument| Type | Description|
| -------   |------ | ----------- |
| `feature_1`  |Feature  | A GeoJSON feature |
| `feature_2`  |Feature    | A GeoJSON feature |

| Return  | Type | Description |
| ------- | ------ | ----------- |
| `difference`  | Feature  | A GeoJSON feature |

```python
from geojson import Polygon, Feature
from turfpy.transformation import difference
f1 = Feature(geometry=Polygon([[
    [128, -26],
    [141, -26],
    [141, -21],
    [128, -21],
    [128, -26]]]), properties={"combine": "yes", "fill": "#00f"})
f2 = Feature(geometry=Polygon([[
    [126, -28],
    [140, -28],
    [140, -20],
    [126, -20],
    [126, -28]]]), properties={"combine": "yes"})
difference(f1, f2)
```

* transform rotate : Rotates any geojson Feature or Geometry of a specified angle, around its centroid or a given pivot point; all rotations follow the right-hand rule

| Argument| Type | Description|
| -------   |------ | ----------- |
| `feature`  |Feature  | A GeoJSON feature |
| `angle`  | float    | angle of rotation (along the vertical axis), from North in decimal degrees, negative clockwise |
| `pivot`  | list(optional)    | point around which the rotation will be performed, deafult values is centroid |
| `mutate`  | boolean(optional)     | allows GeoJSON input to be mutated (significant performance increase if True), deafult value is False |

| Return  | Type | Description |
| ------- | ------ | ----------- |
| `geojson`  | Feature  | The rotated GeoJSON |

```python
from turfpy.transformation import transform_rotate
from geojson import Polygon, Feature
f = Feature(geometry=Polygon([[[0,29],[3.5,29],[2.5,32],[0,29]]]))
pivot = [0, 25]
transform_rotate(f, 10, pivot)
```

* transform translate : Moves any geojson Feature or Geometry of a specified distance along a Rhumb Line on the provided direction angle.

| Argument| Type | Description|
| -------   |------ | ----------- |
| `feature`  |Feature  | A GeoJSON feature |
| `distance`  | float    | length of the motion, negative values determine motion in opposite direction |
| `direction`  | float   | of the motion, angle from North in decimal degrees, positive clockwise |
| `units`  | str(optional)     | Unit of distance, default is 'km' refer [Units type](#units-type) section|
| `z_translation`  | float(optional)     | length of the vertical motion, same unit of distance, default value is 0 |
| `mutate`  | boolean(optional)     | allows GeoJSON input to be mutated (significant performance increase if True), deafult value is False |

| Return  | Type | Description |
| ------- | ------ | ----------- |
| `geojson`  | Feature  | The translated GeoJSON |

```python
from turfpy.transformation import transform_translate
from geojson import Polygon, Feature
f = Feature(geometry=Polygon([[[0,29],[3.5,29],[2.5,32],[0,29]]]))
transform_translate(f, 100, 35, mutate=True)
```

* transform scale : Scale a GeoJSON from a given point by a factor of scaling (ex: factor=2 would make the GeoJSON 200% larger).
If a FeatureCollection is provided, the origin
point will be calculated based on each individual Feature.

| Argument| Type | Description|
| -------   |------ | ----------- |
| `feature`  | Feature | FeatureCollection | A GeoJSON to be scaled |
| `factor`  | float    | factor of scaling, positive or negative values greater than 0 |
| `origin`  | str or list   | Point from which the scaling will occur (string options: sw/se/nw/ne/center/centroid), can also provide a point, deafult value is centroid |
| `mutate`  | boolean(optional)     | allows GeoJSON input to be mutated (significant performance increase if True), deafult value is False |

| Return  | Type | Description |
| ------- | ------ | ----------- |
| `geojson`  | Feature  | The scaled GeoJSON |

```python
from turfpy.transformation import transform_scale
from geojson import Polygon, Feature
f = Feature(geometry=Polygon([[[0,29],[3.5,29],[2.5,32],[0,29]]]))
transform_scale(f, 3, origin=[0, 29])
```

* tesselate : Tesselates a Feature into a FeatureCollection of triangles using earcut.

| Argument| Type | Description|
| -------   |------ | ----------- |
| `poly`  | Feature(Polygon) | the polygon to tesselate |

| Return  | Type | Description |
| ------- | ------ | ----------- |
| `geojson`  | FeatureCollection  | a geometrycollection feature |

```python
from geojson import Feature
from turfpy.transformation import tesselate
polygon = Feature(geometry={"coordinates": [[[11, 0], [22, 4], [31, 0], [31, 11],[21, 15], [11, 11], [11, 0]]], "type": "Polygon"})
tesselate(polygon)
```

* line offset : Takes a linestring or multilinestring and returns a line at offset by the specified distance.

| Argument| Type | Description|
| -------   |------ | ----------- |
| `geojson`  | Feature(Line or MultiLineString) | input GeoJSON of Line or MutliLineString |
| `distance`  | float | distance to offset the line (can be of negative value) |
| `unit`  | str(Optional) | Unit of distance, default is 'km' refer [Units type](#units-type) section |

| Return  | Type | Description |
| ------- | ------ | ----------- |
| `geojson`  | Feature  | Line feature offset from the input line |

```python
from geojson import MultiLineString, Feature
from turfpy.transformation import line_offset
ls = Feature(geometry=MultiLineString([
     [(3.75, 9.25), (-130.95, 1.52)],
     [(23.15, -34.25), (-1.35, -4.65), (3.45, 77.95)]
 ]))
line_offset(ls, 2, unit='mi')
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
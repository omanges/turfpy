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
| `Feature`  | Polygon  | A circle polygon |

```python
from turfpy.transformation import circle
from geojson import Point, Feature
circle(center=Feature(geometry=Point((-75.343, 39.984))), radius=5, steps=10)
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
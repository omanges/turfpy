## Boolean Examples :
* boolean_disjoint : Takes two features and returns (TRUE) if the two geometries do not touch or overlap.

| Argument| Type | Description|
| -------   |------ | ----------- |
| `feature_1`  |Feature  | Feature 1 |
| `feature_2`  |Feature  | Feature 2 |


| Return  | Type | Description |
| ------- | ------ | ----------- |
| `bool`  | bool  | Return true or false |

```python
from geojson import Feature, Point
from turfpy.boolean import boolean_disjoint

feature_1 = Feature(geometry=Point((19.0760, 72.8777)))
feature_2 = Feature(geometry=Point((29.0760, 72.8777)))
boolean_disjoint(feature_1, feature_2)
```

* boolean_intersects : Takes two features and returns (TRUE) if the intersection of the two geometries is NOT an empty set.

| Argument| Type | Description|
| -------   |------ | ----------- |
| `feature_1`  |Feature  | Feature 1 |
| `feature_2`  |Feature  | Feature 2 |

| Return  | Type | Description |
| ------- | ------ | ----------- |
| `bool`  | bool  | Return true or false |

```python
from geojson import Feature, Point
from turfpy.boolean import boolean_intersects

feature_1 = Feature(geometry=Point((19.0760, 72.8777)))
feature_2 = Feature(geometry=Point((29.0760, 72.8777)))
boolean_intersects(feature_1, feature_2)
```

* boolean_within : Takes two features and returns (TRUE) if the intersection of the two geometries is NOT an empty set.

| Argument| Type | Description|
| -------   |------ | ----------- |
| `feature_1`  |Feature  | Feature 1 |
| `feature_2`  |Feature  | Feature 2 |

| Return  | Type | Description |
| ------- | ------ | ----------- |
| `bool`  | bool  | Return true or false |

```python
from geojson import Feature, Point, Polygon
from turfpy.boolean import boolean_within

poly = Polygon(
    [
        [
            (1, 1),
            (1, 10),
            (10, 10),
            (10, 1),
            (1, 1)
        ]
    ]
)

feature_1 = Feature(geometry=Point((4, 4)))
feature_2 = Feature(geometry=poly)
boolean_within(feature_1, feature_2)
```
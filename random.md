## Random Examples :
  * Random Position : Generates a random position, if bbox provided then the generated position will be in the bbox.
  
| Argument  | Type | Description |
| ------- | ------ | ----------- |
| `bbox`  | list  | Bounding Box in which position to be generated |

| Return  | Type | Description |
| ------- | ------ | ----------- |
| `position`  | list  | A position as coordinates|

```python
from turfpy.random import random_position

random_position(bbox=[11.953125, 18.979025953255267, 52.03125, 46.558860303117164])
```

* Random Points : Generates geojson random points, if bbox provided then the generated points will be in the bbox.

| Argument  | Type | Description |
| ------- | ------ | ----------- |
| `count`  | int  | Number of points to be generated, default value is one |
| `bbox`  | list  | Bounding Box in which points are to be generated |

| Return  | Type | Description |
| ------- | ------ | ----------- |
| `points`  | FeatureCollection  | A FeatureCollection of generated points |

```python
from turfpy.random import random_points

random_points(count=3, bbox=[11.953125, 18.979025953255267, 52.03125, 46.558860303117164])
```
## Feature Conversion Examples :
* polygon_to_line : Takes a Polygon or MultiPolygon and convert it to a line.

| Argument| Type | Description|
| -------   |------ | ----------- |
| `polygon`  | Polygon | Multipolygon  | a polygon or multipolygon |
| `options`  | float  | A dict representing additional properties |


| Return  | Type | Description |
| ------- | ------ | ----------- |
| `object`  | Feature | FeatureCollection  | Return a feature or feature collection |

```python
from geojson import Feature, Polygon
from turfpy.feature_conversion import polygon_to_line

feature_1 = Feature(geometry=Polygon([[[0,29],[3.5,29],[2.5,32],[0,29]]]))
polygon_to_line(feature_1)
```

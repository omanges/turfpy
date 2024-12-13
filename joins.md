## Joins Examples :
* points_within_polygon : Find Point(s) that fall within (Multi)Polygon(s).

| Argument    | Type                                                     | Description                                    |
| ------- |   ---------------------------------------------------------- | ---------------------------------------------- |
| `points`    | Feature/FeatureCollection of Points                      | FeatureCollection of Points to find            |
| `polygons`  | Feature/FeatureCollection of Polygon(s)/MultiPolygon(s)  | FeatureCollection of Polygon(s)/MultiPolygon(s)|
| `chunk_size`  | int                                                    | Number of chunks each process to handle. The default value is 1, for a large number of features please use `chunk_size` greater than 1 to get better results in terms of performance.|

| Return      | Type               | Description                                                       |
| ----------- | ------------------ | ----------------------------------------------------------------- |
| `points`    | FeatureCollection  | A FeatureCollection of Points in given Polygon(s)/MultiPolygon(s) |

```python
from geojson import Feature, FeatureCollection, Point, Polygon
from turfpy.joins import points_within_polygon

p1 = Feature(geometry=Point((-46.6318, -23.5523)))
p2 = Feature(geometry=Point((-46.6246, -23.5325)))
p3 = Feature(geometry=Point((-46.6062, -23.5513)))
p4 = Feature(geometry=Point((-46.663, -23.554)))
p5 = Feature(geometry=Point((-46.643, -23.557)))

points = FeatureCollection([p1, p2, p3, p4, p5])

poly = Polygon(
    [
        [
            (-46.653, -23.543),
            (-46.634, -23.5346),
            (-46.613, -23.543),
            (-46.614, -23.559),
            (-46.631, -23.567),
            (-46.653, -23.560),
            (-46.653, -23.543),
        ]
    ]
)
result = points_within_polygon(points, FeatureCollection([poly]))
```
# def center_of_mass(geojson, properties: dict = None):
#     type = get_type(geojson)
#
#     if type == 'Point':
#         point = Point(geojson['coordinates'])
#         return Feature(geometry=point, properties=properties if properties else {})
#     elif type == 'Polygon':
#         coords = []
#
#         def callback_coord_each(coord, coord_index, feature_index, multi_feature_index, geometry_index):
#             nonlocal coords
#             coords.append(coord)
#
#         coord_each(geojson, callback_coord_each)
#
#         centre = centroid(geojson, properties)
#         translation = centre['geometry']['coordinates']
#         sx = 0
#         sy = 0
#         sArea = 0
#
#         neutralizedPoints = []
#
#         for point in coords:
#             neutralizedPoints.append((point[0] - translation[0], point[1] - translation[1]))
#
#         for i in range(0, len(coords)):
#             pi = neutralizedPoints[i]
#             xi = pi[0]
#             yi = pi[1]
#
#             pj = neutralizedPoints[i + 1]
#             xj = pj[0]
#             yj = pj[1]
#
#             a = xi * yj - xj * yi
#
#             sArea += a
#
#             sx += (xi + xj) * a
#             sy += (yi + yj) * a
#
#         if sArea == 0:
#             return centre
#         else:
#             area = sArea * 0.5
#             areaFactor = 1 / (6 * area)
#
#         point = Point(translation[0] + areaFactor * sx, translation[1] + areaFactor * sy)
#
#         return  Feature(geometry=point, properties=properties if properties else {})
#
#     else:
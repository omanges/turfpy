from geojson import Point
import math


def bearing(start: Point, end: Point, final=False):
    """
    Takes two {@link Point} and finds the geographic bearing between them,
    :param Point start: Start point
    :param Point end: Ending point
    :param boolean final:
    :return float: calculates the final bearing if true

    Example :-
    from turfpy import measurement
    from geojson import Point
    start = Point((-75.343, 39.984))
    end = Point((-75.534, 39.123))
    measurement.bearing(start,end)
    """
    if final:
        return calculate_final_bearing(start, end)
    start_coordinates = start['coordinates']
    end_coordinates = end['coordinates']
    lon1 = math.radians(float(start_coordinates[0]))
    lon2 = math.radians(float(end_coordinates[0]))
    lat1 = math.radians(float(start_coordinates[1]))
    lat2 = math.radians(float(end_coordinates[1]))

    a = math.sin(lon2 - lon1) * math.sin(lat2)
    b = (math.cos(lat1) * math.sin(lat2)) - (math.sin(lat1) * math.cos(lat2) * math.cos(lon2 - lon1))
    return math.degrees(math.atan2(a, b))


def calculate_final_bearing(start, end):
    bear = bearing(end, start)
    bear = (bear + 180) % 360
    return bear

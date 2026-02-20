import vector_geom as vg
from enum import IntEnum

class Side(IntEnum):
    LEFT = -1
    COLINEAR = 0
    RIGHT = 1

def side(segment: vg.Segment, point: vg.Point) -> Side:
    """
    Returns a value indicating on which side of a (directed) line segment a point lies.
    See the Side enum.
    Applies only for 2D geometries.
    :param segment: the (directed) segment of whose side to check
    :param point: the point whose side is checked
    :return: an integer representing on which side of the line the point lies
    """
    indicator = (segment.p1.y * (segment.p2.x - point.x)
                 + segment.p2.y * (point.x - segment.p1.x)
                 + point.y * (segment.p1.x - segment.p2.x))
    if indicator < 0:
        return Side.LEFT
    elif indicator > 0:
        return Side.RIGHT
    return Side.COLINEAR

def check_intersect(segment_1: vg.Segment, segment_2: vg.Segment) -> bool:
    """
    Checks whether two line segments intersect.
    This is equivalent to that the endpoints of each segment each lie on opposite sides of the other segment.
    This implementation does NOT allow lines only to touch (at endpoints), but their interiors need to intersect.
    Use of this function is typically faster than computation of an intersection point
    :param segment_1: first line segment
    :param segment_2: one endpoint of the second line segment
    :return: a boolean indicating whether the two line segments intersect
    """
    return (side(segment_1, segment_2.p1) * side(segment_1, segment_2.p2) == -1
            and side(segment_2, segment_1.p1) * side(segment_2, segment_1.p2) == -1)

def point_in_polygon(point: vg.Point, polygon: vg.Polygon) -> bool:
    """
    Checks whether a point is inside a polygon.
    This is equivalent to that a segment starting outside the polygon and ending at the point intersects
    an odd number of edges of the polygon.
    We check with the semiline ((0, y), (x, y))
    TODO: allow for polygons with negative x coordinates.
    :param point: the x-coordinate of the point
    :param polygon: the polygon, as a list of vertices.
    :return: a boolean indicating whether the point lies inside the polygon
    """
    num_intersects = 0
    semiline = vg.Segment(vg.Point(0, point.y), point)
    for s in polygon.segments:
        if check_intersect(s, semiline):
            num_intersects += 1
    return num_intersects % 2 == 1

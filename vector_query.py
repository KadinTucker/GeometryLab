import math

import vector_geom as vg
from enum import IntEnum

# Due to floating point errors, it is necessary to define a tolerance here.
# The user should note that the units they use should be appropriate to the scale used.
POINT_EQUALITY_TOLERANCE = 10e-6

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

def segment_intersects_segment(segment_1: vg.Segment, segment_2: vg.Segment) -> bool:
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

def point_inside_polygon(point: vg.Point, polygon: vg.Polygon) -> bool:
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
        if segment_intersects_segment(s, semiline):
            num_intersects += 1
    return num_intersects % 2 == 1

def project_point_onto_line(point: vg.Point, line: vg.Segment) -> (vg.Point, float):
    l = line.get_length()
    if l == 0:  # Degenerate lines technically exist!
        return line.p1.copy(), 0.0
    scalar_product = ((point.x - line.p1.x) * (line.p2.x - line.p1.x)
                      + (point.y - line.p1.y) * (line.p2.y - line.p1.y)) / l
    return (vg.Point(line.p1.x + (line.p2.x - line.p1.x) * scalar_product / l,
                    line.p1.y + (line.p2.y - line.p1.y) * scalar_product / l),
            scalar_product)

def point_equals_point(point_1: vg.Point, point_2: vg.Point) -> bool:
    return distance_point_point(point_1, point_2) < POINT_EQUALITY_TOLERANCE

def point_inside_line(point: vg.Point, line: vg.Segment) -> bool:
    return point_equals_point(point, project_point_onto_line(point, line)[0])

def point_inside_segment(point: vg.Point, segment: vg.Segment) -> bool:
    proj_point, sp = project_point_onto_line(point, segment)
    return 0 < sp < segment.get_length() and point_equals_point(point, proj_point)

def segment_equals_segment(segment_1: vg.Segment, segment_2: vg.Segment) -> bool:
    return (point_equals_point(segment_1.p1, segment_2.p1) and point_equals_point(segment_1.p2, segment_2.p2)
            or point_equals_point(segment_1.p2, segment_2.p1) and point_equals_point(segment_1.p1, segment_2.p2))

def segment_overlaps_segment(segment_1: vg.Segment, segment_2: vg.Segment) -> bool:
    if segment_equals_segment(segment_1, segment_2):
        return True
    count = sum([point_inside_segment(segment_1.p1, segment_2), point_inside_segment(segment_1.p2, segment_2),
                 point_inside_segment(segment_2.p1, segment_1), point_inside_segment(segment_2.p2, segment_1)])
    return count >= 2

def segment_touches_segment(segment_1: vg.Segment, segment_2: vg.Segment) -> bool:
    # Touches and only touches
    count = sum([point_equals_point(segment_1.p1, segment_2.p1), point_equals_point(segment_1.p1, segment_2.p2),
                 point_equals_point(segment_1.p2, segment_2.p1), point_equals_point(segment_1.p2, segment_2.p2)])
    return count == 1

def linestring_intersects_linestring(linestring_1: vg.LineString, linestring_2: vg.LineString) -> bool:
    for seg1 in linestring_1.segments:
        for seg2 in linestring_2.segments:
            if segment_intersects_segment(seg1, seg2):
                return True
    return False

def linestring_overlaps_linestring(linestring_1: vg.LineString, linestring_2: vg.LineString) -> bool:
    for seg1 in linestring_1.segments:
        for seg2 in linestring_2.segments:
            if segment_overlaps_segment(seg1, seg2):
                return True
    return False

def linestring_crosses_polygon(linestring: vg.LineString, polygon: vg.Polygon) -> bool:
    return (linestring_intersects_linestring(linestring, polygon)
            and not point_inside_polygon(linestring.get_vertex(0), polygon)
            and not point_inside_polygon(linestring.get_vertex(-1), polygon))

def polygon_overlaps_polygon(polygon_1: vg.Polygon, polygon_2: vg.Polygon) -> bool:
    return linestring_intersects_linestring(polygon_1, polygon_2)

def distance_point_point(point_1: vg.Point, point_2: vg.Point):
    return math.hypot(point_1.x - point_2.x, point_1.y - point_2.y)

def distance_point_line(point: vg.Point, line: vg.Segment):
    return distance_point_point(point, project_point_onto_line(point, line)[0])

def distance_point_segment(point: vg.Point, segment: vg.Segment):
    proj_point, sp = project_point_onto_line(point, segment)
    if sp <= 0:
        return distance_point_point(segment.p1, point)
    elif sp >= segment.get_length():
        return distance_point_point(segment.p2, point)
    return distance_point_line(point, segment)

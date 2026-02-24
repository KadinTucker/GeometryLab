import vector_geom as vg

def construct_point_copy(point: vg.Point):
    return vg.Point(point.x, point.y)

def construct_point_by_offset(point: vg.Point, direction: vg.Segment):
    return vg.Point(point.x + direction.p2.x - direction.p1.x, point.y + direction.p2.y - direction.p1.y)

def construct_point_along_segment(segment: vg.Segment, length_fraction: float):
    if length_fraction > 1 or length_fraction < 0:
        raise ValueError("Length fraction must be between 0 and 1")
    return vg.Point(segment.p1.x + (segment.p2.x - segment.p1.x) * length_fraction,
                    segment.p1.y + (segment.p2.y - segment.p1.y) * length_fraction)

def construct_point_along_linestring(linestring: vg.LineString, length_fraction: float):
    if length_fraction > 1 or length_fraction < 0:
        raise ValueError("Length fraction must be between 0 and 1")
    lengths = [seg.get_length() for seg in linestring.segments]
    total_length = sum(lengths)
    accum_length = 0
    index = 0
    while accum_length < total_length * length_fraction:
        accum_length += lengths[index + 1]

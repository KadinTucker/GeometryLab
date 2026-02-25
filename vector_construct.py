import vector_geom as vg

def construct_point_copy(point: vg.Point):
    return vg.Point(point.x, point.y)

def construct_point_by_offset(point: vg.Point, offset: vg.Segment):
    return vg.Point(point.x + offset.p2.x - offset.p1.x, point.y + offset.p2.y - offset.p1.y)

def construct_point_along_segment_fraction(segment: vg.Segment, length_fraction: float):
    if length_fraction > 1 or length_fraction < 0:
        raise ValueError("Length fraction must be between 0 and 1")
    return vg.Point(segment.p1.x + (segment.p2.x - segment.p1.x) * length_fraction,
                    segment.p1.y + (segment.p2.y - segment.p1.y) * length_fraction)

def construct_point_along_segment_absolute(segment: vg.Segment, length_absolute: float):
    l = segment.get_length()
    return vg.Point(segment.p1.x + (segment.p2.x - segment.p1.x) * length_absolute / l,
                    segment.p1.y + (segment.p2.y - segment.p1.y) * length_absolute / l)

def construct_point_along_linestring_absolute(linestring: vg.LineString, length_absolute: float):
    lengths = [seg.get_length() for seg in linestring.segments]
    total_length = sum(lengths)
    if length_absolute > total_length or length_absolute < 0:
        raise ValueError("Length fraction must be between 0 and 1")
    length_remain = total_length - lengths[0]
    index = 0
    while length_remain > lengths[index + 1]:
        index += 1
        length_remain -= lengths[index + 1]
    return construct_point_along_segment_absolute(linestring.segments[index], length_remain)

def construct_point_along_linestring_fraction(linestring: vg.LineString, length_fraction: float):
    if length_fraction > 1 or length_fraction < 0:
        raise ValueError("Length fraction must be between 0 and 1")
    return construct_point_along_linestring_absolute(linestring, length_fraction * linestring.get_length())

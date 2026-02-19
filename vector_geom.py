import math
from enum import Enum

class GeometryType(Enum):
    GEOMETRY = 0
    POINT = 1
    SEGMENT = 2
    LINESTRING = 3
    POLYGON = 4

class Geometry:

    def __init__(self):
        self.type = GeometryType.GEOMETRY

    def get_length(self):
        return 0

    def get_area(self):
        return 0.0

class Point(Geometry):

    def __init__(self, x: float, y: float):
        super().__init__()
        self.type = GeometryType.POINT
        self.x = x
        self.y = y

    def as_tuple(self):
        return self.x, self.y

    def __str__(self):
        return f"({self.x}, {self.y})"

class Segment:

    def __init__(self, p1: Point, p2: Point):
        super().__init__()
        self.type = GeometryType.SEGMENT
        self.p1 = p1
        self.p2 = p2

    def get_length(self):
        return distance_point_point(self.p1, self.p2)

    def __str__(self):
        return f"{self.p1}->{self.p2}"

class LineString:

    def __init__(self, vertices: list[Point]):
        super().__init__()
        self.type = GeometryType.LINESTRING
        self.vertices = vertices
        self.segments = [Segment(vertices[i], vertices[i+1]) for i in range(len(vertices) - 1)]

    def append_vertex(self, vertex: Point):
        self.vertices.append(vertex)
        if len(self.vertices) > 1:
            self.segments.append(Segment(self.vertices[-2], vertex))

    def insert_vertex(self, vertex: Point, index):
        self.vertices.insert(index, vertex)
        self.segments.insert(index - 1, Segment(self.vertices[index - 1], self.vertices[index]))
        self.segments[index] = Segment(self.vertices[index], self.vertices[index + 1])

    def get_length(self):
        return sum([s.get_length() for s in self.segments])

    def __str__(self):
        return "-".join(map(str, self.vertices))

class Polygon(LineString):

    def __init__(self, vertices: list[Point]):
        super().__init__(vertices)
        self.type = GeometryType.POLYGON
        self.segments = [Segment(vertices[i-1], vertices[i]) for i in range(len(vertices))]

    def append_vertex(self, vertex: Point):
        self.vertices.append(vertex)
        self.segments.insert(0, Segment(vertex, self.vertices[0]))
        if len(self.vertices) > 1:
            self.segments[-1] = Segment(self.vertices[-2], self.vertices[-1])


    def __str__(self):
        return "-".join(map(str, self.vertices + [self.vertices[0]]))

def distance_point_point(p1: Point, p2: Point):
    return math.hypot(p1.x - p2.x, p1.y - p2.y)

def distance_point_segment(p: Point, s: Segment):
    # Complex!
    pass

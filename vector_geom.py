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

    def copy(self):
        return Geometry()

class Point(Geometry):

    def __init__(self, x: float, y: float):
        super().__init__()
        self.type = GeometryType.POINT
        self.x = x
        self.y = y

    def as_tuple(self):
        return self.x, self.y

    def copy(self):
        return Point(self.x, self.y)

    def __str__(self):
        return f"({self.x}, {self.y})"

class Segment:

    def __init__(self, p1: Point, p2: Point):
        super().__init__()
        self.type = GeometryType.SEGMENT
        self.p1 = p1
        self.p2 = p2

    def get_length(self):
        return math.hypot(self.p1.x - self.p2.x, self.p1.y - self.p2.y)

    def get_direction(self):
        l = self.get_length()
        return (self.p2.x - self.p1.x) / l, (self.p2.y - self.p1.y) / l

    def copy(self):
        return Segment(self.p1.copy(), self.p2.copy())

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

    def reverse(self):
        self.vertices.reverse()
        self.segments.reverse()

    def get_vertex(self, index):
        return self.vertices[index].copy()

    def get_length(self):
        return sum([s.get_length() for s in self.segments])

    def copy(self):
        return LineString([vert.copy() for vert in self.vertices])

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

    def change_zero_vertex(self, to_index):
        if to_index >= len(self.vertices) or to_index < 0:
            raise ValueError(f"Index {to_index} out of range")
        for i in range(to_index):
            self.vertices.append(self.vertices.pop(0))
            self.segments.append(self.segments.pop(0))

    def copy(self):
        return Polygon([vert.copy() for vert in self.vertices])

    def __str__(self):
        return "-".join(map(str, self.vertices + [self.vertices[0]]))


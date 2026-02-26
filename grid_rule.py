import transform as tf
import vector_geom as vg

"""
A "grid rule" is a pair of functions:
 - "project": given two unsigned integer coordinates (rows and columns), output a "cell coordinate"
 - "query": given a real world coordinate, either get a well-defined grid coordinate or "Not in grid".
    A more complete version can give the inverse images of the query function: i.e., sets of real-world points
    that map to each grid cell - a more complete interpretation of the "project" function.
Furthermore, the two functions should agree: that is:
 - project(query(X, Y)) = (X, Y)
 - query(project(r, c)) = (r, c)
Example grid rules:
 - Raster - square grid
   - Raster with uniform affine transformation
 - Hexagonal coordinates - different parametrizations are possible
 - Latitude, Longitude (i.e., grids need not be a regular tiling).
 - Cylindrical coordinates with fixed radius (such as Mercator projection)
Grids can optionally support topological queries through neighbourhood definitions.
 - "Neighbours" function: Given a grid coordinate (r, c), which grid coordinates (r', c') are neighbours of (r, c)?
 - The neighbours function should be structure-preserving:
   - if (r', c') is a neighbour of (r, c), then the closure of the union of the sets
     query^-1 (r', c') and query^-1(r, c) is connected.
"""

class Grid:
    # TODO: make Grid support data types other than float
    def __init__(self, origin: vg.Point, scale: float, n_rows: int, n_cols: int):
        self.origin = origin
        self.scale = scale
        # indexed by row, col
        self._cells = [[0.0 for _ in range(n_cols)] for _ in range(n_rows)]

    def get_num_rows(self):
        return len(self._cells)

    def get_num_cols(self):
        return len(self._cells[0])

    def check_index(self, r: int, c: int):
        if not (0 <= r < self.get_num_rows() and 0 <= c < self.get_num_cols()):
            raise IndexError(f"Index {(r, c)} not valid for grid of {self.get_num_rows()} rows "
                             f"by {self.get_num_cols()} columns")

    def project(self, r: int, c: int) -> vg.Point:
        # To be overridden
        self.check_index(r, c)
        return self.origin.copy()

    def is_in_extent(self, point: vg.Point) -> bool:
        # To be overridden
        return False

    def query(self, point: vg.Point) -> (int, int):
        # To be overridden
        if not self.is_in_extent(point):
            raise ValueError("Error: point not inside grid bounds")
        return 0, 0

    def get_support(self, r: int, c: int) -> vg.Polygon:
        return vg.Polygon([])

    def get_value(self, r: int, c: int) -> float:
        self.check_index(r, c)
        return self._cells[r][c]

    def set_value(self, r: int, c: int, value: float) -> None:
        self.check_index(r, c)
        self._cells[r][c] = value

class RasterGrid(Grid):

    def __init__(self, origin: vg.Point, scale: float, n_rows: int, n_cols: int,
                 transform=tf.transform_identity):
        super().__init__(origin, scale, n_rows, n_cols)
        self.transform = transform

    def project(self, r: int, c: int) -> vg.Point:
        self.check_index(r, c)
        offset = self.transform(vg.Point((c + 0.5) * self.scale, (r + 0.5) * self.scale))
        return vg.Point(self.origin.x + offset.x, self.origin.y + offset.y)

    def get_support(self, r: int, c: int) -> vg.Polygon:
        self.check_index(r, c)
        return vg.Polygon([self.transform(vg.Point(c * self.scale, r * self.scale)),
                           self.transform(vg.Point((c + 1) * self.scale, r * self.scale)),
                           self.transform(vg.Point((c + 1) * self.scale, (r + 1) * self.scale)),
                           self.transform(vg.Point(c * self.scale, (r + 1) * self.scale))])

    def query(self, point: vg.Point) -> (int, int):
        rel_point = vg.Point(point.x - self.origin.x, point.y - self.origin.y)
        query_point = self.transform.inverse(rel_point)
        r = int(query_point.y / self.scale)
        c = int(query_point.x / self.scale)
        if not (0 <= r < self.get_num_rows() and 0 < c <= self.get_num_cols()):
            raise ValueError(f"Point {point} not inside grid bounds")
        return r, c


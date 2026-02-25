# Geometric Objects

In GeometryLab, objects exist in an abstracted 2-dimensional space.

A _geometric object_ is an object that takes up some of that space. GeometryLab primarily supports _vector objects_:
- Points (single, infinitesimally small locations)
- Line Segments (the portions of a line between two points)
- Line Strings (a connected sequence of line segments)
- Polygons (areas enclosed by line strings)

A single object is considered homogeneous, though objects can also be split into multiple objects. Some objects are 
called _multipart objects_ and, while considered a single object, consist of multiple individual objects (though 
restricted to being the same type). The individual objects are called its _parts_, and they may be disjoint or 
overlapping. A multipart object's parts must not themselves consist of more than one part.

## Actions 

### Measures

Line segments have a _length_ measure. Line Strings have a length equal to the sum of the lengths of their components. 

Polygons have an _area_ and a _perimeter_. 

### Topological Queries

Topological queries are queries related to the interaction between multiple objects. Topological queries take the form
of yes-no questions: more detailed answers can be obtained through measures and set operations (see further). 

Topological relationships between objects are fully described through the _9-intersection model_. The 9-intersection 
model models relationships between two geometric objects by the intersections of their topological interiors, exteriors,
and boundaries, and the (covering) dimensions thereof. 

Common named topological relationships can be queried. However, more primitive relationships can also be queried:
 - Disjoint: no common points
 - Touching: non-disjoint, but all common points are boundary points
   - Polygon - Polygon (eq. two segments are nontrivially colinear)
   - Line String - Line String (eq. length of intersection == 0, intersection non-empty)
   - Polygon - Line String (eq. no points of the line string are inside the polygon)
 - Containment: one object contains all points of another
   - Point inside Polygon (eq. any infinite line containing the point intersects the polygon boundary oddly many times)
   - Line String/Polygon inside Polygon (eq. all vertices of the line string/polygon are within the polygon; 
   or at least one vertex within the polygon and no intersection with the polygon boundary)
   - Point inside Line Segment (eq. the point lies on the line spanning the line segment's vertices and is "between" 
   them)
 - Crossing: the interiors of the objects intersect, but the boundaries/endpoints of the crossing object lies outside 
the object
   - Line String crosses Polygon (eq. the two end points, i.e. boundary, of the linestring are outside the polygon)
   - Line String crosses Line String (eq. the two line strings have intersecting interiors)

### Distance Queries

_Proximity queries_ are queries based on distances (numbers). These queries have numeric answers to the question: what
is the distance between two objects? In this instance, we are specifically considering Euclidean distance. 

For points, given a metric, the distance between objects is well-defined. However, when it comes to other geometries,
there can be different notions of distance. In general, when speaking of the distance between two objects, it is the
_shortest distance_ between those objects. There are other notions of distances between objects, but they are currently
not considered.

### Context Queries

When multiple objects exist together in a defined context, so-called _context relationships_ can be defined: these are
relationships that may depend on all existing objects. The most common example of a context relationship is the 
_nearest_ relationship. An object A is _nearest_ to another object B if the shortest distance from A to B is shorter
than the distance from A to any other object C. By extension, the _n-nearest_ relationship can be defined as including
the _n_ closest objects to an object.

Context queries can also include selection queries, in which all objects in a context satisfying some condition are 
output as a selection. The condition can be a topological relationship or a threshold on a distance relationship. 

With large numbers of objects, context queries can become computationally complex. To solve this, objects are spatially
indexed, which effectively reduces the number of objects to consider. 

### Constructions

_Construction_ in GeometryLab refers to creating new geometric objects relative to existing ones. Constructions can be 
thought of as analogous to mathematical "formal constructions", the system of geometry in which lines and circles can be
constructed and copied, but not measured. 

The goal of constructions is to create geometric objects bounded by rules, but with a high level of flexibility for the
constructor. These new objects are always created relative to an existing, reference object, or multiple, as may be
required.

Direction is a key component of constructions, and it can be defined either as a vector, given input coordinates or 
taken from a line segment, or it can be produced from a bearing (angle). 

Production:
- Point: copy a point; given a point, produce an exact copy of it
- Point: given origin (point), direction, and distance
- Point: given line string, length fraction
- Point: given line string, absolute length along
- Segment: given origin (point) and destination (point)
  - Can naturally be combined with constructing a point relative to another to produce a line segment with given length
  and direction
- Point: given a source object and a destination object, construct the nearest point on the destination object to the 
source object. Optionally, if the destination object is a segment, treat it as though infinitely extended
- Segment: given two geometric objects, construct the shortest line segment between them
- Segment: given an origin, direction, and geometric object, construct the segment from the origin in the direction
that extends just far enough to intersect the geometric object.

Selection:
- Point: given a LineString (or Polygon) and an index, retrieve the vertex at that index.
- Segment: given a LineString and an index, retrieve that segment.
- LineString: given a Polygon, retrieve its perimeter (geometry) as a LineString.
- Point: given a source object and a destination object, select the nearest vertex on the destination object to the 
source object. 

Modification:
- Polygon: given an index, change the arbitrary "start" point to the given index.
- LineString or Polygon: given a point, append or insert this point to the LineString/Polygon.
- LineString or Polygon: given an index, remove that vertex, while connecting the others.
- LineString or Polygon: reverse the order of vertices in the object.
- LineString: given a point on a LineString or a segment crossing the LineString, split the LineString into two, 
at that point
- Polygon: given a LineString that crosses a polygon, split the polygon into two by that LineString

Transformation:
- Translation: given a direction and distance, move all vertices of an object by some amount in that direction.
- Rotation: relative to a point and given an angle, rotate all vertices of an object by that angle.
- Reflection: relative to a line (represented by (1) segment or (2) point and direction), reflect all vertices of an 
object over that line.
- Dilation: given a fixed point and a scale factor, uniformly dilate all vertices of an object.

These operations can also be chained (e.g., insert the midpoint of a segment to its linestring). The parameters of each
operation should also be taken from the geometries themselves:
- Lengths of Segments;
- Vertices (Point) of Segments and LineStrings;
- Points along Segments, LineStrings, and Polygons (by distance or by dimensionless fraction);
- Directions of Segments.
  - Left or right orthogonals of Segments
  - Interior or exterior orthogonals of Polygons

#### Advanced Constructions

Some constructions are less intuitive while mathematically well-defined. However, some of their parameters may also 
require fine-tuning. 

- Polygon: given a set of points, construct their Convex Hull. Optionally, a threshold length can be defined to make a
"concave hull". 
- Polygons: given a set of points, construct their Delaunay Triangulation as a number of polygon objects. 
- Polygons: given a set of points, construct their Voronoi Diagram as a number of polygon objects. Optionally, may define
a polygonal region in which the Voronoi polygons may extend; by default, this is the convex hull of the input points. 
- Polygon: the common "buffer" operation; given a geometric object and a distance, construct the area (approximated by
a polygon within that distance from the geometric object). May optionally decide how densely to approximate buffers or
how to treat vertices. 

### Boolean Operations

Boolean operations in vector geometry refers to the set _union_, _intersection_, and _complementation_ operations. In 
this context, complementation is not supported, but the set _difference_ operation is. Union and intersection operations
are symmetric, but difference is not. 

The results of boolean operations may produce multipart objects. It is recommended to avoid using multipart objects if
it can be avoided, and to split them apart appropriately! 

Not all boolean operations are supported due to boundary constraints or triviality. Some operations that may be 
understood as boolean operations, such as "splitting", are instead implemented as constructions; the user is directed 
to Constructions if this is the goal.

The supported operations include:
- Polygon union Polygon
- Polygon intersect Polygon
- Polygon minus Polygon
- Polygon intersect LineString
- Polygon intersect Point
- LineString union LineString
- LineString intersect LineString
- LineString minus LineString
- LineString intersect Point

### Generalization

_Generalization_ refers to reducing the level of detail or dimensionality of a geometric representation
of an object. Geometric generalization takes a variety of forms, with different procedures taking different approaches. 
The user is encouraged to try their own generalization 

_Simplification_ is the process of removing detail (i.e., vertices) from an object. Methods to identify the most 
important vertices to keep can vary; the simplistic method of removing every n'th vertex is supported, as well as the
more sophisticated Douglas-Peucker algorithm.

_Smoothing_ refers to the modification of vertices to reduce the angles between line segments in an object while 
preserving the overall shape. Gaussian smoothing is supported. 

_Skeletonizing_ is the process of converting a polygon to one or more LineStrings. As with other generalization methods,
approaches may vary.

## Smooth Geometries

Some common geometric objects are poorly modelled by vectors and are instead better modelled by parametric curves and 
areas. Examples include:
- Circles
- Ellipses
- Hermite curves



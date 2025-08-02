#from your_module import point_in_polygon  # Import the auxiliary function from your codebase
from check_belonging_to_polygon import point_position_with_respect_to_polygon as point_in_polygon
from interpolate_points import interpolate_points
from math import sqrt

def triangle_centroid(a, b, c):
    """Compute centroid of triangle defined by points a, b, c."""
    return ((a[0] + b[0] + c[0]) / 3.0, (a[1] + b[1] + c[1]) / 3.0)

def max_perimeter(a, b, c):
    return 2*(max(a[0],b[0],c[0]) - min(a[0],b[0],c[0])) + 2*(max(a[1],b[1],c[1]) - min(a[1],b[1],c[1]))

def distance(a,b):
    pass

def generate_points_from_polygon_in(input_points, tempo = 1):
    """
    Given a list of 2D points representing a simple polygon (vertices in order),
    returns a list of points created as follows:
    For every consecutive triplet of vertices (wrapping cyclically),
    compute the centroid of the triangle,
    if the centroid lies inside the polygon (according to imported point_in_polygon),
    include centroid in output list;
    otherwise include the middle vertex of the triplet.

    Args:
        input_points: list of (x, y) tuples representing polygon vertices.

    Returns:
        List of (x, y) tuples of generated points.
    """
    n = len(input_points)
    if n < 3:
        raise ValueError("Polygon must have at least 3 vertices to form triangles.")

    result = []
    for i in range(n):
        a = input_points[(i - 1) % n]
        b = input_points[(i + 0) % n]
        c = input_points[(i + 1) % n]
        triangle_is_completely_inner = True
        for j, other_points in enumerate(input_points):
            if j == (i - 1) % n or j == i or j == (i + 1) % n:
                continue
            if point_in_polygon(input_points[j], [a, b, c]) == "inner":
                triangle_is_completely_inner = False
        if triangle_is_completely_inner:
            quasiperimeter = max_perimeter(a,b,c)
            centroid = triangle_centroid(a, b, c)
            if point_in_polygon(centroid, input_points) == "inner":
                interpolant = interpolate_points(b, centroid, tempo/sqrt(quasiperimeter))
                result.append(interpolant)
            else:
                result.append(b)
        else:
            result.append(b)

    return result

def generate_points_from_polygon_out(input_points, tempo=1):
    """
    Given a list of 2D points representing a simple polygon (vertices in order),
    returns a list of points created as follows:
    For every consecutive triplet of vertices (wrapping cyclically),
    compute the centroid of the triangle,
    if the centroid lies outside the polygon (according to imported point_in_polygon),
    include centroid in output list;
    otherwise include the middle vertex of the triplet.

    Args:
        input_points: list of (x, y) tuples representing polygon vertices.

    Returns:
        List of (x, y) tuples of generated points.
    """
    n = len(input_points)
    if n < 3:
        raise ValueError("Polygon must have at least 3 vertices to form triangles.")

    result = []
    for i in range(n):
        a = input_points[(i - 1) % n]
        b = input_points[(i + 0) % n]
        c = input_points[(i + 1) % n]

        triangle_is_completely_outer = True
        for j, other_points in enumerate(input_points):
            if j == (i - 1) % n or j == i or j == (i + 1) % n:
                continue
            if point_in_polygon(input_points[j], [a, b, c]) == "inner":
                triangle_is_completely_outer = False
        if triangle_is_completely_outer:
            quasiperimeter = max_perimeter(a,b,c)
            centroid = triangle_centroid(a, b, c)
            if point_in_polygon(centroid, input_points) == "outer":
                interpolant = interpolate_points(b, centroid, tempo/sqrt(quasiperimeter))
                result.append(interpolant)
            else:
                result.append(b)
        else:
            result.append(b)
    return result

def orientation_type(points, epsilon=1e-12):
    """
    Helper function to compute orientation of three points.
    Returns one of {"clockwise", "counterclockwise", "collinear", "degenerate"}.
    """
    p1, p2, p3 = [tuple(map(float, pt)) for pt in points]
    if len({p1, p2, p3}) < 3:
        return "degenerate"
    cross = (p2[0] - p1[0]) * (p3[1] - p1[1]) - (p2[1] - p1[1]) * (p3[0] - p1[0])
    if abs(cross) < epsilon:
        return "collinear"
    elif cross > 0:
        return "counterclockwise"
    else:
        return "clockwise"

def is_point_on_segment(p, a, b, epsilon=1e-12):
    """
    Check if point p lies exactly on the line segment a-b.
    Uses collinearity and bounding box checks with tolerance epsilon.
    """
    orient = orientation_type([a, b, p], epsilon)
    if orient != "collinear":
        return False
    
    min_x, max_x = sorted([a[0], b[0]])
    min_y, max_y = sorted([a[1], b[1]])
    return (min_x - epsilon <= p[0] <= max_x + epsilon) and (min_y - epsilon <= p[1] <= max_y + epsilon)

def point_in_polygon(point, polygon, epsilon=1e-12):
    """
    Ray casting algorithm for point-in-polygon test excluding boundary.
    Returns True if point is strictly inside polygon,
    False if outside.
    """
    x, y = point
    inside = False
    n = len(polygon)
    
    for i in range(n):
        j = (i - 1) % n  # Previous vertex index
        xi, yi = polygon[i]
        xj, yj = polygon[j]

        # Check if edge intersects horizontal ray from point to the right
        # Condition: point's y between edge's ys, and intersection x > x of point
        if ((yi > y) != (yj > y)):
            # Compute intersection of edge with horizontal line at y
            intersect_x = (xj - xi) * (y - yi) / (yj - yi + 1e-20) + xi
            if intersect_x > x + epsilon:
                inside = not inside
    
    return inside

def point_position_with_respect_to_polygon(point, polygon, epsilon=1e-12):
    """
    Determine position of a 2D point relative to a simple polygon.

    Returns one of {"outer", "inner", "edge", "vertex"}.

    Args:
        point: tuple (x,y) coordinates of point.
        polygon: list of tuples [(x0,y0), (x1,y1), ...] polygon vertices.
        epsilon: numerical tolerance for closeness checks.

    Returns:
        String describing point's position relative to polygon.
    """
    # Check if point matches any vertex (within epsilon)
    for v in polygon:
        if abs(point[0] - v[0]) <= epsilon and abs(point[1] - v[1]) <= epsilon:
            return "vertex"

    # Check if point lies on any polygon edge
    n = len(polygon)
    for i in range(n):
        a = polygon[i]
        b = polygon[(i + 1) % n]
        if is_point_on_segment(point, a, b, epsilon):
            return "edge"
    
    # Check inside/outside using ray casting algorithm (excluding boundary)
    if point_in_polygon(point, polygon, epsilon):
        return "inner"
    else:
        return "outer"

def triangle_contains_no_other_points(triangle_pts, all_points, exclude_indices):
    """Return True if no other points except exclude_indices are inside the triangle."""
    v1, v2, v3 = triangle_pts
    for idx, pt in enumerate(all_points):
        if idx in exclude_indices:
            continue
        if point_in_triangle(pt, v1, v2, v3):
            return False
    return True

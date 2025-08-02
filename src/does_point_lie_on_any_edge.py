from src.point_on_segment import point_on_segment

def does_point_lie_on_any_edge(point_idx, points, edges):
    """Return True if point lies exactly on any polygon edge segment."""
    p = points[point_idx]
    for (i, j) in edges:
        a = points[i]
        b = points[j]
        if point_on_segment(p, a, b):
            return True
    return False

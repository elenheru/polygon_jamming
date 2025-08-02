def third_vertex(triangle, edge):
    """Return the third vertex index in triangle not in edge."""
    for v in triangle:
        if v not in edge:
            return v
    return None

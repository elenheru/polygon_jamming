
def edge_key(i, j):
    """Return sorted tuple for edge key."""
    return (min(i, j), max(i, j))

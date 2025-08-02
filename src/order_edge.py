def order_edges(edges_set):
    """
    Given a set of integer pairs (edges), returns an ordered list of tuples such that:
    - Each tuple in the returned list is present in the input set either as is or reversed.
    - The tuples form a continuous chain where consecutive edges share exactly one endpoint.
    - If ordering is not possible, raises ValueError.

    Args:
        edges_set: set of tuples (int, int)

    Returns:
        List of tuples representing the ordered edges with proper orientation.

    Raises:
        ValueError: if edges cannot be sequenced properly.
    """
    if not edges_set:
        return []

    # Build adjacency: map vertex -> set of edges connected to it
    from collections import defaultdict, deque

    # Normalize edges: store edges with min < max to identify undirected edges cleanly
    undirected_edges = set(tuple(sorted(edge)) for edge in edges_set)

    # Build adjacency list per vertex for undirected graph
    vertex_edges = defaultdict(set)
    for u, v in undirected_edges:
        vertex_edges[u].add((u, v))
        vertex_edges[v].add((u, v))

    # Check connectivity and vertices degrees to ensure chain or cycle is possible
    # Find start vertex: vertex with degree 1 if path, or any vertex if cycle
    end_points = [v for v, es in vertex_edges.items() if len(es) == 1]
    if len(end_points) not in [0, 2]:
        # More/fewer than allowed endpoints for Euler path/cycle
        raise ValueError("Input edges cannot be arranged into a proper chain or cycle.")

    # If cycle, pick any vertex; if path, start from endpoint
    start_vertex = end_points[0] if end_points else next(iter(vertex_edges))

    # Prepare to reconstruct the path by walking edges
    used_edges = set()
    path = []

    current_vertex = start_vertex

    while True:
        # Find unused edge connected to current_vertex
        available_edges = [e for e in vertex_edges[current_vertex] if e not in used_edges]
        if not available_edges:
            # No more edges from here
            break

        edge = available_edges[0]
        used_edges.add(edge)

        # Determine edge orientation to append
        if edge[0] == current_vertex:
            oriented_edge = edge
            next_vertex = edge[1]
        else:
            oriented_edge = (edge[1], edge[0])
            next_vertex = edge[0]

        path.append(oriented_edge)
        current_vertex = next_vertex

    if len(used_edges) != len(undirected_edges):
        # Not all edges used -> disconnected components or cannot form chain
        raise ValueError("Input edges cannot be arranged into a proper chain; edges unused.")

    return path

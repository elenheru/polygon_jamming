from src.edge_key import edge_key
from src.third_vertex import third_vertex


def insert_missing_points_with_full_triangle_edges(points, edges, tri):
    """
    Insert missing points by adding all edges of the triangle formed with polygon edge.

    Conditions:
    - Triangle contains no other point inside except its vertices.
    """
    polygon_vertices = set()
    for e in edges:
        polygon_vertices.update(e)

    missing_points = set(range(len(points))) - polygon_vertices

    # Prepare edge to triangles mapping for quick lookup
    edge_to_triangles = dict()
    for simplex in tri.simplices:
        for k in range(3):
            e = edge_key(simplex[k], simplex[(k + 1) % 3])
            if e not in edge_to_triangles:
                edge_to_triangles[e] = []
            edge_to_triangles[e].append(simplex)

    inserted_any = True
    while inserted_any and missing_points:
        inserted_any = False
        edges_list = list(edges)
        for missing_idx in list(missing_points):
            for e in edges_list:
                triangles = edge_to_triangles.get(e, [])
                for simplex in triangles:
                    v_third = third_vertex(simplex, e)
                    if v_third != missing_idx:
                        continue

                    i, j = e
                    triangle_pts = points[[i, j, v_third]]
                    exclude_indices = {i, j, v_third}

                    if triangle_contains_no_other_points(triangle_pts, points, exclude_indices):
                        # Remove old edge and add all triangle edges
                        edges.discard(e)
                        new_edges = [
                            edge_key(i, j),
                            edge_key(j, v_third),
                            edge_key(v_third, i)
                        ]
                        for ne in new_edges:
                            edges.add(ne)

                        missing_points.remove(missing_idx)
                        inserted_any = True
                        break
                if inserted_any:
                    break
            if inserted_any:
                break

    return edges

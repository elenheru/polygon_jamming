from scipy.spatial import Delaunay

from src.edge_key import edge_key
from src.third_vertex import third_vertex
from src.does_point_lie_on_any_edge import does_point_lie_on_any_edge
from src.insert_missing_points_with_full_triangle_edges import insert_missing_points_with_full_triangle_edges

def build_polygon_edges(points):
    # Step 1: Initial edges from convex hull
    hull = Delaunay(points).convex_hull
    edges = set()
    for e in hull:
        edges.add(edge_key(e[0], e[1]))

    # Step 2: Delaunay triangulation
    tri = Delaunay(points)

    # Build edge to triangles mapping
    edge_to_triangles = dict()
    for simplex in tri.simplices:
        for k in range(3):
            e = edge_key(simplex[k], simplex[(k+1) % 3])
            if e not in edge_to_triangles:
                edge_to_triangles[e] = []
            edge_to_triangles[e].append(simplex)

    # Step 3: Iterative edge replacement based on your condition
    changed = True
    while changed:
        changed = False
        edges_list = list(edges)
        for e in edges_list:
            tris = edge_to_triangles.get(e, [])
            for simplex in tris:
                v_third = third_vertex(simplex, e)
                if not does_point_lie_on_any_edge(v_third, points, edges):
                    # Replace edge e with other two edges of triangle
                    edges.discard(e)
                    i, j = e
                    k = v_third
                    new_edges = [edge_key(i, k), edge_key(j, k)]
                    for ne in new_edges:
                        edges.add(ne)
                    changed = True
                    break
            if changed:
                break

    # Step 4: Enhanced insertion of missing points with full triangle edges
    edges = insert_missing_points_with_full_triangle_edges(points, edges, tri)

    return edges, tri

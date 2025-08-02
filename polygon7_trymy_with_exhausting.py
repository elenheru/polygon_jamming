import pygame
import numpy as np
from scipy.spatial import Delaunay

FPS = 48
RESOLUTION = (1024, 1024)
BACKGROUND_COLOR = (10, 10, 10)

NUM_POINTS = 24
POINT_RADIUS = 3
POINT_COLOR = (255, 215, 0)    # Gold/yellow
EDGE_COLOR = (0, 255, 255)     # Cyan

def edge_key(i, j):
    """Return sorted tuple for edge key."""
    return (min(i, j), max(i, j))

def point_on_segment(p, a, b, eps=1e-9):
    """Check if point p lies on segment a-b (colinear and between)."""
    ap = p - a
    ab = b - a
    cross = np.cross(ab, ap)
    if abs(cross) > eps:
        return False
    dot = np.dot(ap, ab)
    if dot < 0:
        return False
    if dot > np.dot(ab, ab):
        return False
    return True

def segments_intersect(p1, p2, q1, q2):
    """Check if segments (p1,p2) and (q1,q2) intersect."""
    def orientation(a, b, c):
        val = (b[1]-a[1])*(c[0]-b[0]) - (b[0]-a[0])*(c[1]-b[1])
        if abs(val) < 1e-14:
            return 0
        return 1 if val > 0 else 2

    o1 = orientation(p1, p2, q1)
    o2 = orientation(p1, p2, q2)
    o3 = orientation(q1, q2, p1)
    o4 = orientation(q1, q2, p2)

    if o1 != o2 and o3 != o4:
        return True

    if o1 == 0 and point_on_segment(q1, p1, p2):
        return True
    if o2 == 0 and point_on_segment(q2, p1, p2):
        return True
    if o3 == 0 and point_on_segment(p1, q1, q2):
        return True
    if o4 == 0 and point_on_segment(p2, q1, q2):
        return True

    return False

def third_vertex(triangle, edge):
    """Return the third vertex index in triangle not in edge."""
    for v in triangle:
        if v not in edge:
            return v
    return None

def does_point_lie_on_any_edge(point_idx, points, edges):
    """Return True if point lies exactly on any polygon edge segment."""
    p = points[point_idx]
    for (i, j) in edges:
        a = points[i]
        b = points[j]
        if point_on_segment(p, a, b):
            return True
    return False

def point_in_triangle(pt, v1, v2, v3):
    """Check if point pt lies inside triangle (v1,v2,v3) using barycentric technique."""
    def sign(p1, p2, p3):
        return (p1[0] - p3[0])*(p2[1] - p3[1]) - (p2[0] - p3[0])*(p1[1] - p3[1])

    b1 = sign(pt, v1, v2) < 0.0
    b2 = sign(pt, v2, v3) < 0.0
    b3 = sign(pt, v3, v1) < 0.0

    return ((b1 == b2) and (b2 == b3))

def triangle_contains_no_other_points(triangle_pts, all_points, exclude_indices):
    """Return True if no other points except exclude_indices are inside the triangle."""
    v1, v2, v3 = triangle_pts
    for idx, pt in enumerate(all_points):
        if idx in exclude_indices:
            continue
        if point_in_triangle(pt, v1, v2, v3):
            return False
    return True

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

    return edges

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

def generate_points_and_polygon():
    points = np.random.rand(NUM_POINTS, 2) * np.array(RESOLUTION)
    edges = build_polygon_edges(points)
    return points, edges

def main():
    pygame.init()
    screen = pygame.display.set_mode(RESOLUTION)
    pygame.display.set_caption("Polygon Edges with Enhanced Point Insertion")
    clock = pygame.time.Clock()

    points, edges = generate_points_and_polygon()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    # Regenerate polygon on backspace key press
                    points, edges = generate_points_and_polygon()

        screen.fill(BACKGROUND_COLOR)

        # Draw polygon edges
        for (i, j) in edges:
            pygame.draw.aaline(screen,
                               EDGE_COLOR,
                               points[i].astype(int),
                               points[j].astype(int))

        # Draw points
        for p in points:
            pygame.draw.circle(screen,
                              POINT_COLOR,
                              p.astype(int),
                              POINT_RADIUS)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()

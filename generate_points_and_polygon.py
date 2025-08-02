import numpy as np
from constant_parameters import *
from build_polygon_edges import build_polygon_edges
from order_edge import order_edges as sort_edges

def generate_points_and_polygon(points=None):
    if points is None:
        points = np.random.rand(NUM_POINTS, 2) * np.array(RESOLUTION)
    edges, triangulation = build_polygon_edges(points)
    _edges = sort_edges(edges)
    _points = list()
    for e in _edges:
        # _points.append(points[e[0]].astype(int))
        _points.append((points[e[0]][0],points[e[0]][1]))
    return points, _edges, triangulation, _points

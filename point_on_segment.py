import numpy as np

def point_on_segment(p, a, b, eps=1e-9):
    """Check if point p lies on segment a-b (colinear and between)."""
    ap = np.subtract(np.asarray(p),np.asarray(a))
    ab = np.subtract(np.asarray(b),np.asarray(a))
    cross = np.cross(ab, ap)
    if abs(cross) > eps:
        return False
    dot = np.dot(ap, ab)
    if dot < 0:
        return False
    if dot > np.dot(ab, ab):
        return False
    return True

def interpolate_points(p1, p2, t):
    """
    Linearly interpolate between two 2D points p1 and p2 with parameter t.
    If t is outside [0,1], it is clipped to that range.
    
    Args:
        p1: tuple of two floats/ints (x1, y1)
        p2: tuple of two floats/ints (x2, y2)
        t: float interpolation parameter, ideally in [0, 1]
        
    Returns:
        tuple (x, y) interpolated point
    """
    t = max(0.0, min(1.0, t))  # Clip t to [0, 1]
    x = (1 - t) * p1[0] + t * p2[0]
    y = (1 - t) * p1[1] + t * p2[1]
    return (x, y)

from orientation import orientation

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

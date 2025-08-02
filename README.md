# polygon_jamming
Visualisation of algorithm on polygon. AI assistant is Perplexity.

The algorithm iteratively takes polygon and moves vertices, so that they compose another polygon, which completely lies inside original one. 
Shape of resulting polygons converge into some oval which lies inside the original polygon.
Only two dimensional simple (non degenerate) polygons are being considered.

The core idea of transfoming procedure is to move a vertex in (or towards) position of centroid of triangle,
which is build on sequential triplet of polygon vertices.
Direct application of this idea comes across with a problem, that centroid is not necessarily lies inside polygon given.
Same problem remains even we only take a small move towards centroid.

Rigorous checks of whether candidate point lies inside polygon or not are being made on every step.

Also, we can invert the movement, and let polygon expand. 
This option is not of that much interest, because it always produces a polygon tantamount to convex hull of initial one.


Usage:
- Run the main file. 
- Press Backspace key to generate new polygon. 
- Press Page Up key to start/stop expansion of polygon.
- Press Page Down key to start/stop jamming of polygon.

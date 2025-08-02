import pygame as pg
import numpy as np
from scipy.spatial import Delaunay

from src import constant_parameters
from src.generate_points_and_polygon import generate_points_and_polygon
from src.check_belonging_to_polygon import point_position_with_respect_to_polygon as pprp
from src.jammer import generate_points_from_polygon_in as jam_in
from src.jammer import generate_points_from_polygon_out as jam_out

def main():
    pg.init()
    screen = pg.display.set_mode(constant_parameters.RESOLUTION)
    pg.display.set_caption("Polygon Edges with Enhanced Point Insertion")
    clock = pg.time.Clock()
    font = pg.font.SysFont(None, 18)
    points, edges, triangulation, ordered_vertices = generate_points_and_polygon()
    running = True
    skip_edges = False
    draw_labels = False
    jamming = False
    expanding = False
    triangulation_already_drawn = False
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_q:
                    running = False
                if event.key == pg.K_PAGEUP:
                    expanding = not expanding
                    jamming = False
                if event.key == pg.K_PAGEDOWN:
                    jamming = not jamming
                    expanding = False
                if event.key == pg.K_BACKSPACE:
                # Regenerate polygon on backspace key press
                    screen.fill(constant_parameters.BACKGROUND_COLOR)
                    skip_edges = False
                    points, edges, triangulation, ordered_vertices = generate_points_and_polygon()
                    triangulation_already_drawn = False

        # to see trajectories
        screen.fill(constant_parameters.BACKGROUND_COLOR, special_flags=pg.BLEND_RGBA_MAX)
        #screen.fill(constant_parameters.BACKGROUND_COLOR)

        # Draw inner triangulation edges
        for (p1i, p2i, p3i) in triangulation.simplices:
            if triangulation_already_drawn:
                break
            pg.draw.aaline(screen,
                               constant_parameters.TRIANGULATION_EDGE_COLOR,
                               points[p1i],
                               points[p2i])
            pg.draw.aaline(screen,
                               constant_parameters.TRIANGULATION_EDGE_COLOR,
                               points[p2i],
                               points[p3i])
            pg.draw.aaline(screen,
                               constant_parameters.TRIANGULATION_EDGE_COLOR,
                               points[p3i],
                               points[p1i])
        triangulation_already_drawn = True
        # Draw polygon edges
        for n in range(len(ordered_vertices)):
            if skip_edges:
                continue
            pg.draw.aaline(screen,
                               constant_parameters.EDGE_COLOR,
                               ordered_vertices[n-1],
                               ordered_vertices[n])
        # skip_edges = True

        # Draw points
        for n, v in enumerate(ordered_vertices):
            pg.draw.circle(screen,
                               ((10 * n + 30) % 256, 15, 0),
                               (v[0], v[1]),
                               constant_parameters.POINT_RADIUS)


        if draw_labels:
            # Draw a cursor
            mouse_x, mouse_y = pg.mouse.get_pos()
            pg.draw.circle(screen,
                               constant_parameters.CURSOR_COLOR,
                               (mouse_x, mouse_y),
                               1)

            pg.draw.circle(screen,
                               constant_parameters.CURSOR_COLOR,
                               (mouse_x, mouse_y),
                               constant_parameters.CURSOR_RADIUS * 0,
                               1)

            # Put label of mouse position
            text_surface = font.render(f"Mouse: ({mouse_x}, {mouse_y})", True, constant_parameters.CURSOR_COLOR, (0,0,0))
            screen.blit(text_surface, (10, 10))

            # Put label of point type
            text_surface = font.render(f"Point is: {pprp((mouse_x, mouse_y), ordered_vertices)}", True, constant_parameters.CURSOR_COLOR, (0,0,0))
            screen.blit(text_surface, (10, 30))


        pg.display.flip()
        clock.tick(constant_parameters.FPS)
        if jamming:
            ordered_vertices = jam_in(ordered_vertices, tempo=constant_parameters.JAMMING_TEMPO)
        if expanding:
            ordered_vertices = jam_out(ordered_vertices, tempo=constant_parameters.JAMMING_TEMPO)
    pg.quit()


if __name__ == "__main__":
    main()

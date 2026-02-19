import sys

import pygame
import vector_geom as vg

def draw_point(point, surface, color, weight, transform_func):
    pygame.draw.circle(surface, color, transform_func(point.as_tuple()), weight)

def draw_segment(segment, surface, color, weight, transform_func):
    pygame.draw.line(surface, color, transform_func(segment.p1.as_tuple()),
                     transform_func(segment.p2.as_tuple()), weight)

def draw_linestring(linestring, surface, color, weight, transform_func):
    for segment in linestring.segments:
        draw_segment(segment, surface, color, weight, transform_func)

def draw_polygon(polygon, surface, color, transform_func):
    if len(polygon.vertices) >= 3:
        pygame.draw.polygon(surface, color, [transform_func(v.as_tuple()) for v in polygon.vertices])

class VectorWindow:

    def __init__(self):
        self.world_origin = (0, 0)
        self.world_extent = (100, 100)
        self.pixel_origin = (0, 0)
        self.pixel_extent = (300, 300)
        self.objects = []

    def draw(self, surface):
        for obj in self.objects:
            if obj.type == vg.GeometryType.POINT:
                draw_point(obj, surface, (255, 0, 0), 5, self.transform)
            elif obj.type == vg.GeometryType.SEGMENT:
                draw_segment(obj, surface, (0, 255, 0), 5, self.transform)
            elif obj.type == vg.GeometryType.LINESTRING:
                draw_linestring(obj, surface, (0, 255, 0), 5, self.transform)
            elif obj.type == vg.GeometryType.POLYGON:
                draw_polygon(obj, surface, (0, 0, 255), self.transform)

    def transform(self, world_coord):
        return ((world_coord[0] - self.world_origin[0]) / self.world_extent[0] * self.pixel_extent[0],
                (world_coord[1] - self.world_origin[1]) / self.world_extent[1] * self.pixel_extent[1])

    def detransform(self, pixel_coord):
        return (pixel_coord[0] * self.world_extent[0] / self.pixel_extent[0] + self.world_origin[0],
                pixel_coord[1] * self.world_extent[1] / self.pixel_extent[1] + self.world_origin[1])

    def drag_pan(self):
        pass


if __name__ == '__main__':
    pygame.init()
    display = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()

    v_window = VectorWindow()
    construct_mode = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                # pressing c places a new point
                # if in generic construction mode, constructs a point object
                # if in linestring construction mode, adds the point to the linestring
                if event.key == pygame.K_c:
                    x, y = v_window.detransform(pygame.mouse.get_pos())
                    if construct_mode == 0:
                        v_window.objects.append(vg.Point(x, y))
                    elif construct_mode == 1 or construct_mode == 2:
                        v_window.objects[-1].append_vertex(vg.Point(x, y))
                # pressing v enters or exits linestring construction mode
                elif event.key == pygame.K_v:
                    if construct_mode != 1:
                        v_window.objects.append(vg.LineString([]))
                        construct_mode = 1
                    else:
                        construct_mode = 0
                # pressing b enters or exits polygon construction mode
                elif event.key == pygame.K_b:
                    if construct_mode != 2:
                        v_window.objects.append(vg.Polygon([]))
                        construct_mode = 2
                    else:
                        construct_mode = 0

        display.fill((0, 0, 0))
        v_window.draw(display)
        # Draw most recently placed point if not in point construct mode
        if construct_mode != 0:
            if len(v_window.objects[-1].vertices) > 0:
                draw_point(v_window.objects[-1].vertices[-1], display, (255, 0, 0), 5, v_window.transform)
            if construct_mode == 2 and len(v_window.objects[-1].vertices) > 1:
                draw_point(v_window.objects[-1].vertices[-2], display, (255, 255, 0), 5, v_window.transform)
        pygame.display.update()
        clock.tick(20)

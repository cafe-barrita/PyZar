import pygame
from vector_2d import Vector


class Window:
    def __init__(self, pos, res, map_res):
        self.__pos = Vector(*pos)
        self.res = Vector(*res)
        self.__map_res = Vector(*map_res)

    @property
    def pos(self):
        return self.__pos

    @pos.setter
    def pos(self, pos):
        bottom_right = pos + self.res
        print('pos:', bottom_right)
        if pos.x >= 0:
            if pos.y >= 0:
                if bottom_right.x < self.__map_res.x:
                    if bottom_right.y < self.__map_res.y:
                        self.__pos = pos
                    else:
                        self.pos = Vector(pos.x, self.__map_res.y - self.res.y - 1)
                else:
                    self.pos = Vector(self.__map_res.x - self.res.x - 1, pos.y)
            else:
                self.pos = Vector(pos.x, 0)
        else:
            self.pos = Vector(0, pos.y)

    def move(self, scroll_vector: Vector):
        pos = self.__pos - scroll_vector
        bottom_right = pos + self.res
        if pos.x >= 0 and pos.y >= 0 and bottom_right.x < self.__map_res.x and bottom_right.y < self.__map_res.y:
            self.__pos = pos
            return True
        return False


class MiniMap:
    def __init__(self, window: Window, map_res, terrain, stuff):
        # FIXME esto no vale para mapas que no sean cuadrados
        sides = Vector(150, 150)
        self.window = window
        self.factor = map_res[0] / sides.x
        self.margin = 10
        # sides = Vector(*map_res) / self.factor
        self.pos = Vector(self.margin, window.res[1] - self.margin - sides.y)
        self.center = self.pos + window.res / (2 * self.factor)
        self.window_points = (
            self.pos,
            self.pos + Vector(window.res.x, 0) / self.factor,
            self.pos + window.res / self.factor,
            self.pos + Vector(0, window.res.y) / self.factor,
        )
        self.window_tuples = tuple((p + window.pos / self.factor).int() for p in self.window_points)
        self.points = (
            (self.margin - 1, window.res.y - self.margin + 1),
            (self.margin + sides.x + 1, window.res.y - self.margin + 1),
            (self.margin + sides.x + 1, window.res.y - self.margin - sides.y - 1),
            (self.margin - 1, window.res.y - self.margin - sides.y - 1),
        )
        xs = [int(point[0]) for point in self.points]
        ys = [int(point[1]) for point in self.points]
        self.x_bounds = min(xs), max(xs)
        self.y_bounds = min(ys), max(ys)
        self.terrain = terrain
        terrain.set_minimap_data(self.pos, sides)
        self.stuff = stuff

    def click(self, point: Vector):
        if self.x_bounds[1] >= point.x >= self.x_bounds[0] and self.y_bounds[1] >= point.y >= self.y_bounds[0]:
            point = (point - self.center) * self.factor
            # print('CLICK', point)
            self.window.pos = point
            self.screen_move(self.window.pos)
            return Vector(0, 0)

    def draw(self, screen):
        pygame.draw.polygon(screen, (0, 0, 0), self.points)
        self.terrain.draw_for_minimap(screen)
        pygame.draw.polygon(screen, (255, 255, 0), self.points, 3)
        pygame.draw.polygon(screen, (200, 255, 0), self.window_tuples, 2)

    def screen_move(self, window_pos):
        self.window_tuples = tuple((p + window_pos / self.factor).int() for p in self.window_points)

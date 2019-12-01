import random
from abc import ABC, abstractmethod
from typing import Tuple

import pygame
from vector_2d import Vector

from items_base_classes import Collective


class Borders:
    def __init__(self, resolution: Tuple[int, int]):
        self.resolution = resolution
        self.margin = 15

    def get_hovered(self, mouse: Vector):
        if mouse.x < self.margin:
            return Vector(1, 0)
        if mouse.x > self.resolution[0] - self.margin:
            return Vector(-1, 0)
        if mouse.y < self.margin:
            return Vector(0, 1)
        if mouse.y > self.resolution[1] - self.margin:
            return Vector(0, -1)


class Item:
    def __init__(self, pos):
        self._pos = self._screen_pos = pos

    @abstractmethod
    def is_instantiable(self):
        raise TypeError(f'{self.__class__.__name__} is an abstract class and is not instantiable')

    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, value):
        self._pos = value

    def __str__(self):
        return self.__class__.__name__

    def __hash__(self):
        return hash(self._pos)


class RoundItem(Item, ABC):
    radius = None
    color = None

    def is_point_inside(self, point):
        return abs(point - self._pos) <= self.radius

    def draw(self, surface: pygame.Surface):
        pygame.draw.circle(surface, self.color, self._screen_pos.int(), 5, 0)


class SquareItem(Item, ABC):
    radius = None
    color = None

    def __init__(self, pos: Vector):
        super().__init__(pos)
        self.points = None
        self._screen_points = None
        self.segments = None
        self.x_bounds = None
        self.y_bounds = None
        self.calc_pos()

    # @property
    # def screen_pos(self):
    #     return self._screen_pos

    def screen_move(self, scroll_vector):
        self._screen_pos += scroll_vector
        self._screen_points = [(Vector(*point) + scroll_vector).int() for point in self._screen_points]

    def calc_pos(self):
        points = (self._pos + Vector(self.radius, self.radius), self._pos + Vector(-self.radius, self.radius),
                  self._pos + Vector(-self.radius, -self.radius), self._pos + Vector(self.radius, -self.radius),)
        self.points = self._screen_points = tuple(point.int() for point in points)
        self.segments = tuple((points[i - 1], points[i]) for i in range(len(points) - 1, -1, -1))
        xs = [int(point.x) for point in points]
        ys = [int(point.y) for point in points]
        self.x_bounds = min(xs), max(xs)
        self.y_bounds = min(ys), max(ys)

    def is_point_inside(self, point):
        return self.x_bounds[1] >= point.x >= self.x_bounds[0] and self.y_bounds[1] >= point.y >= self.y_bounds[0]

    def draw(self, surface: pygame.Surface):
        pygame.draw.polygon(surface, self.color, self._screen_points)


class Resource:
    load = None

    def has_been_worked(self):
        self.load -= 10

    def is_alive(self):
        return self.load > 0


class Mineral(Resource, SquareItem):
    color = 255, 150, 100
    radius = 20

    def __init__(self, pos: Vector):
        self.radius = Mineral.radius
        Resource.__init__(self)
        SquareItem.__init__(self, pos)
        self.load = 8000

    def is_instantiable(self):
        return True


class Tree(Resource, RoundItem):
    color = 100, 200, 10
    radius = 5

    def __init__(self, pos: Vector):
        super().__init__(pos)
        self._pos = pos
        # TODO self.load = 100
        self.load = 30

    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, value):
        self._pos = value

    def is_instantiable(self):
        return True


class Forest(Collective):
    def __init__(self, res, obstacles):
        tree_set = set()
        for _ in range(200):
            x = random.randrange(res[0])
            y = random.randrange(res[1])
            inside = any([obstacle.is_point_inside(Vector(x, y)) for obstacle in obstacles])
            if not inside:
                tree_set.add(Tree(Vector(x, y)))
        super().__init__(tree_set)

    def discard(self, element):
        self.collection.discard(element)


class Building(SquareItem, ABC):
    def __init__(self, pos: Vector):
        super().__init__(pos)


class Castle(Building):
    radius = 30

    def __init__(self, pos: Vector):
        super().__init__(pos)
        self.color = 0, 100, 200

    def is_instantiable(self):
        return True

    def draw(self, surface: pygame.Surface):
        pygame.draw.polygon(surface, self.color, self._screen_points)

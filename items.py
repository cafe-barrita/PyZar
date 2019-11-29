import abc
import random
from abc import ABC
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
    color = None
    radius = None

    @abc.abstractmethod
    def is_instantiable(self):
        raise TypeError(f'{self.__class__.__name__} is an abstract class and is not instantiable')

    def draw(self, surface: pygame.Surface):
        pygame.draw.circle(surface, self.color, self._pos.int(), 5, 0)

    def __str__(self):
        return self.__class__.__name__

    def __hash__(self):
        return hash(repr(self._pos))

    def is_point_inside(self, point):
        return abs(point - self._pos) <= self.radius


class Obstacle:
    radius = None

    def __init__(self, pos: Vector):
        self._pos = pos
        self.points = None
        self.segments = None
        self.x_bounds = None
        self.y_bounds = None
        self.calc_pos()

    def is_point_inside(self, point):
        return self.x_bounds[1] >= point.x >= self.x_bounds[0] and self.y_bounds[1] >= point.y >= self.y_bounds[0]

    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, value):
        self._pos = value
        self.calc_pos()

    def calc_pos(self):
        points = (self._pos + Vector(self.radius, self.radius), self._pos + Vector(-self.radius, self.radius),
                  self._pos + Vector(-self.radius, -self.radius), self._pos + Vector(self.radius, -self.radius),)
        self.points = tuple(point.int() for point in points)
        self.segments = tuple((points[i - 1], points[i]) for i in range(len(points) - 1, -1, -1))
        xs = [int(point.x) for point in points]
        ys = [int(point.y) for point in points]
        self.x_bounds = min(xs), max(xs)
        self.y_bounds = min(ys), max(ys)


class Resource(Item, ABC):
    load = None

    def has_been_worked(self):
        self.load -= 10

    def is_alive(self):
        return self.load > 0


class Mineral(Resource, Obstacle):
    color = 255, 150, 100
    radius = 20

    def __init__(self, pos: Vector):
        Resource.__init__(self)
        Obstacle.__init__(self, pos)
        self.load = 8000

    def is_instantiable(self):
        return True

    def draw(self, surface: pygame.Surface):
        pygame.draw.polygon(surface, self.color, self.points)


class Tree(Resource):
    color = 100, 200, 10
    radius = 5

    def __init__(self, pos: Vector):
        self._pos = pos
        # TODO self.load = 100
        self.load = 30

    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, value):
        self._pos = value

    def pos_increment(self, value):
        self._pos += value

    def is_instantiable(self):
        return True


class Forest(Collective):
    def __init__(self, res, obstacles):
        self.__tree_set = set()
        for _ in range(200):
            x = random.randrange(res[0])
            y = random.randrange(res[1])
            inside = any([obstacle.is_point_inside(Vector(x, y)) for obstacle in obstacles])
            if not inside:
                self.__tree_set.add(Tree(Vector(x, y)))

    def draw(self, screen: pygame.Surface):
        for tree in self.__tree_set:
            tree.draw(screen)

    def discard(self, element):
        self.__tree_set.discard(element)

    def __iter__(self):
        return iter(self.__tree_set)

    def __add__(self, other):
        return list(self.__tree_set) + other

    def __radd__(self, other):
        return list(self.__tree_set) + other


class Building(Item, Obstacle, ABC):
    def __init__(self, pos: Vector):
        # Item.__init__(self, pos)
        Obstacle.__init__(self, pos)


class Castle(Building):
    radius = 30

    def __init__(self, pos: Vector):
        super().__init__(pos)
        self.color = 0, 100, 200

    def is_instantiable(self):
        return True

    def draw(self, surface: pygame.Surface):
        pygame.draw.polygon(surface, self.color, self.points)

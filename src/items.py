import random
from abc import ABC, abstractmethod
from typing import Tuple

import pygame
from vector_2d import Vector


class Borders:
    def __init__(self, resolution: Tuple[int, int]):
        self.resolution = resolution
        self.margin = 15

    def get_hovered(self, mouse: Vector):
        if mouse.x < self.margin:
            return Vector(5, 0)
        if mouse.x > self.resolution[0] - self.margin:
            return Vector(-5, 0)
        if mouse.y < self.margin:
            return Vector(0, 5)
        if mouse.y > self.resolution[1] - self.margin:
            return Vector(0, -5)


class Item:
    def __init__(self, pos, window_pos: Vector):
        self._pos = pos
        self._screen_pos = pos - window_pos
        # print(self.__class__.__name__, self._screen_pos)

    @abstractmethod
    def is_instantiable(self):
        raise TypeError(f'{self.__class__.__name__} is an abstract class and is not instantiable')

    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, value):
        self._pos = value

    @abstractmethod
    def is_point_inside(self, point):
        raise NotImplementedError

    def __str__(self):
        return self.__class__.__name__

    def __hash__(self):
        return hash(self._pos)


class RoundItem(Item, ABC):
    radius = None
    color = None

    def is_point_inside(self, point):
        return abs(point - self._pos) <= self.radius

    def screen_move(self, scroll_vector):
        self._screen_pos += scroll_vector

    def draw(self, surface: pygame.Surface):
        pygame.draw.circle(surface, self.color, self._screen_pos.int(), 5, 0)


class SquareItem(Item, ABC):
    radius = None
    color = None

    def __init__(self, pos: Vector, window_pos: Vector):
        super().__init__(pos, window_pos)
        self.points = None
        self._screen_points = None
        self.segments = None
        self.x_bounds = None
        self.y_bounds = None
        self.calc_pos()

    def screen_move(self, scroll_vector):
        self._screen_pos += scroll_vector
        self._screen_points = [(Vector(*point) + scroll_vector).int() for point in self._screen_points]

    def calc_pos(self):
        screen_points = (
            self._screen_pos + Vector(self.radius, self.radius), self._screen_pos + Vector(-self.radius, self.radius),
            self._screen_pos + Vector(-self.radius, -self.radius),
            self._screen_pos + Vector(self.radius, -self.radius),)
        points = (self._pos + Vector(self.radius, self.radius), self._pos + Vector(-self.radius, self.radius),
                  self._pos + Vector(-self.radius, -self.radius), self._pos + Vector(self.radius, -self.radius),)
        self._screen_points = tuple(point.int() for point in screen_points)
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

    def __init__(self, pos: Vector, window_pos: Vector):
        self.radius = Mineral.radius
        Resource.__init__(self)
        SquareItem.__init__(self, pos, window_pos)
        self.load = 8000

    def is_instantiable(self):
        return True


class Tree(Resource, RoundItem):
    color = 100, 200, 10
    radius = 5

    def __init__(self, pos: Vector, window_pos: Vector):
        super().__init__(pos, window_pos)
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


class Building(SquareItem, ABC):
    ...
    # def __init__(self, pos: Vector, window_pos: Vector):
    #     super().__init__(pos, window_pos)


class Castle(Building):
    radius = 30

    def __init__(self, pos: Vector, window_pos: Vector):

        super().__init__(pos, window_pos)
        self.color = 0, 100, 200

    def is_instantiable(self):
        return True

    def draw(self, surface: pygame.Surface):
        pygame.draw.polygon(surface, self.color, self._screen_points)


class Collective(ABC):
    def __init__(self, collection):
        self.collection = collection

    def screen_move(self, vector: Vector):
        for element in self:
            element.screen_move(vector)

    def actualize(self, surface: pygame.Surface, t: int):
        for element in self:
            element.actualize(surface, t)

    def draw(self, screen: pygame.Surface):
        for e in self:
            e.draw(screen)

    def __iter__(self):
        return iter(self.collection)

    def __add__(self, other):
        return list(self.collection) + other

    def __radd__(self, other):
        return list(self.collection) + other


class Forest(Collective):
    def __init__(self, map_resolution, obstacles, window_pos: Vector):
        tree_set = set()
        for _ in range(1000):
            x = random.randrange(map_resolution[0])
            y = random.randrange(map_resolution[1])
            inside = any([obstacle.is_point_inside(Vector(x, y)) for obstacle in obstacles])
            if not inside:
                tree_set.add(Tree(Vector(x, y), window_pos))
        super().__init__(tree_set)

    def discard(self, element):
        self.collection.discard(element)

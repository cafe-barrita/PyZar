import abc
import random
from abc import ABC

import pygame
from vector_2d import Vector


class Item:
    color = None
    radius = None

    @abc.abstractmethod
    def is_instantiable(self):
        raise TypeError(f'{self.__class__.__name__} is an abstract class and is not instantiable')

    def __init__(self, pos: Vector):
        if self.is_instantiable():
            self.pos = pos

    def draw(self, surface: pygame.Surface):
        pygame.draw.circle(surface, self.color, self.pos.int(), 5, 0)

    def __str__(self):
        return self.__class__.__name__

    def __hash__(self):
        return hash(repr(self.pos))


class Obstacle:
    radius = None

    def __init__(self, pos: Vector):
        points = (pos + Vector(self.radius, self.radius), pos + Vector(-self.radius, self.radius),
                  pos + Vector(-self.radius, -self.radius), pos + Vector(self.radius, -self.radius),)
        self.points = tuple(point.int() for point in points)
        self.segments = tuple((points[i - 1], points[i]) for i in range(len(points) - 1, -1, -1))

    def is_point_inside(self, point):
        # FIXME mejorar esto
        return abs(point - self.pos) <= self.radius * 1.3


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
        Resource.__init__(self, pos)
        Obstacle.__init__(self, pos)
        self.load = 8000
        # self.points = [point.int() for point in (
        #     pos + Vector(Mineral.radius, Mineral.radius), pos + Vector(-Mineral.radius, Mineral.radius),
        #     pos + Vector(-Mineral.radius, -Mineral.radius), pos + Vector(Mineral.radius, -Mineral.radius),)]

    def is_instantiable(self):
        return True

    def draw(self, surface: pygame.Surface):
        pygame.draw.polygon(surface, self.color, self.points)


class Tree(Resource):
    color = 100, 200, 10
    radius = 5

    def __init__(self, pos: Vector):
        super().__init__(pos)
        self.load = 30

    def is_instantiable(self):
        return True


class Forest:
    def __init__(self, res):
        self.tree_set = set()
        for _ in range(200):
            x = random.randrange(res[0])
            y = random.randrange(res[1])
            self.tree_set.add(Tree(Vector(x, y)))

    def draw(self, screen: pygame.Surface):
        for tree in self.tree_set:
            tree.draw(screen)


class Building(Item, Obstacle, ABC):
    def __init__(self, pos: Vector):
        Item.__init__(self, pos)
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

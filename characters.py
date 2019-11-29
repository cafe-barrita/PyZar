import abc
from collections import deque
from typing import Union, List, Deque

import pygame
from vector_2d import Vector

import cursors
from items import Item, Mineral, Tree, Building, Forest, Obstacle


class Character(Item, Obstacle, abc.ABC):
    vel_mod = None
    cursors = None
    radius = 5
    sight_radius = 25

    def __init__(self, pos: Vector):
        Item.__init__(self, pos)
        Obstacle.__init__(self, pos)
        self._destination: Deque[Vector, ...] = deque([pos])
        self._is_pressed = False
        self.obstacle = None

    @property
    def director_vector(self):
        # todo meybe unit vector * radius
        if self.destination:
            return self.destination - self.pos
        else:
            return Vector()

    @property
    def destination(self):
        if self._destination:
            return self._destination[-1]

    @destination.setter
    def destination(self, value):
        self._destination.append(value)

    def append_left_destination(self, value):
        self._destination.appendleft(value)

    def move(self, t: int) -> bool:
        # FIXME esto seguro se puede ordenar un poco
        if self.destination:
            if self.obstacle and self.obstacle.is_point_inside(self.destination):
                if abs(self.pos - self.obstacle.pos) <= (self.radius + self.obstacle.radius):
                    self._destination.pop()
                    return True
                else:
                    self.pos += self.director_vector.unit() * self.vel_mod * t
                    return False
            elif abs(self.director_vector) > self.radius:
                self.pos += self.director_vector.unit() * self.vel_mod * t
                return False
            else:
                self._destination.pop()
                return True

    def draw(self, surface: pygame.Surface):
        pygame.draw.circle(surface, self.color, self.pos.int(), self.radius, 0)
        if self._is_pressed:
            pygame.draw.circle(surface, (0, 255, 0), self.pos.int(), self.radius, 1)

        for dest in self._destination:
            pygame.draw.circle(surface, (255, 0, 0), dest.int(), 1, 1)

    def actualize(self, surface: pygame.Surface, t: int):
        self.move(t)
        self.draw(surface)

    def set_pressed(self, value: bool):
        self._is_pressed = value

    def get_cursor(self, item: Item):
        return self.cursors.get(item.__class__.__name__, pygame.cursors.arrow)

    def is_point_inside(self, point):
        return abs(point - self.pos) <= self.radius * 2


class Farmer(Character):
    vel_mod = 0.05
    color = 0, 0, 255
    cursors = {'Tree': cursors.compiled_axe,
               'Building': cursors.compiled_shovel,
               'Mineral': cursors.compiled_pick,
               }
    radius = 10
    UNEMPLOYED = 'unemployed'
    CHOPPER = 'chopper'
    MINER = 'miner'

    def __init__(self, pos: Vector, home: Building, forest: Forest):
        super().__init__(pos)
        self.work_cycle = [self.get_back_from_work, self.work, self.go_to_work]
        self.__work_cycle_index = -1
        self.job = None
        self.load = 0
        self.work_speed = 0.01
        self.home = home
        self.status = Farmer.UNEMPLOYED
        self.forest = forest

    @property
    def work_cycle_index(self):
        return self.__work_cycle_index

    @work_cycle_index.setter
    def work_cycle_index(self, value):
        if value < -len(self.work_cycle):
            self.__work_cycle_index = -1
        else:
            self.__work_cycle_index = value

    def get_back_from_work(self, t: int):
        self.move(t)
        # if abs(self.pos - self.home.pos) <= self.radius + self.home.radius:
        if self.home.is_point_inside(self.pos + self.director_vector.unit() * self.radius * 2):
            self.load = 0
            self._destination.pop()
            self.destination = self.job.pos
            self.work_cycle_index -= 1

    def work(self, t: int):
        self.load += self.work_speed * t
        # print(f'Load of {str(self.job)}:', self.load)
        if self.load >= 10:
            self.job.has_been_worked()
            if not self.job.is_alive():
                if isinstance(self.job, Tree):
                    self.forest.tree_set.discard(self.job)
                self.job = None
                if self.destination:
                    self._destination.pop()
            self.destination = self.home.pos
            self.work_cycle_index -= 1

    def go_to_work(self, t: int):
        self.move(t)
        if abs(self.pos - self.job.pos) <= self.radius + self.job.radius + 2:
            self.work_cycle_index -= 1
            self._destination.pop()

    def set_job(self, item: Union[Mineral, Tree]):
        self.job = item
        self.destination = item.pos
        if isinstance(item, Tree):
            self.status = Farmer.CHOPPER
        if isinstance(item, Mineral):
            self.status = Farmer.MINER

    def actualize(self, surface: pygame.Surface, t):
        if self.job:
            self.work_cycle[self.work_cycle_index](t)
            self.draw(surface)
        elif self.status == Farmer.CHOPPER:
            for tree in self.forest.tree_set:
                # FIXME que sea el más cercano
                if abs(tree.pos - self.pos) < 100:
                    self.job = tree
                    return
            self.status = Farmer.UNEMPLOYED
            self.__work_cycle_index = -1

        else:
            super().actualize(surface, t)

    def is_instantiable(self):
        return True

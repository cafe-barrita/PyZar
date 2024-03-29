import abc
from typing import Union

import pygame
from vector_2d import Vector

import cursors
from items import Item, Mineral, Tree, Building


class Character:
    vel_mod = None
    color = None
    cursors = None
    radius = 5

    def __init__(self, pos: Vector):
        if self.is_instantiable():
            self.pos = pos
            self._destination = pos
            self._is_pressed = False

    @abc.abstractmethod
    def is_instantiable(self):
        raise TypeError(f'{self.__class__.__name__} is an abstract class and is not instantiable')

    def move(self, t) -> bool:
        dif = self._destination - self.pos
        if abs(dif) > 1:
            self.pos += dif.unit() * self.vel_mod
            return False
        else:
            return True

    def draw(self, surface: pygame.Surface):
        pygame.draw.circle(surface, self.color, self.pos.int(), 5, 0)
        if self._is_pressed:
            pygame.draw.circle(surface, (0, 255, 0), self.pos.int(), 5, 1)

    def actualize(self, surface: pygame.Surface, t):
        self.move(t)
        self.draw(surface)

    def set_pressed(self, value: bool):
        self._is_pressed = value

    def __hash__(self):
        return hash(repr(self.pos))

    def set_destination(self, destination: Vector):
        self._destination = destination

    def get_cursor(self, item: Item):
        return self.cursors[item.__class__.__name__]


class Farmer(Character):
    vel_mod = 1
    color = 0, 0, 255
    cursors = {'Tree': cursors.compiled_axe,
               'Building': cursors.compiled_shovel,
               'Mineral': cursors.compiled_pick,
               }

    def __init__(self, pos: Vector, home: Building):
        super().__init__(pos)
        self.work_cycle = [self.go_back, self.work, self.go]
        self.__work_cycle_index = -1
        self.job = None
        self.load = 0
        self.work_speed = 0.001
        self.home = home

    @property
    def work_cycle_index(self):
        return self.__work_cycle_index

    @work_cycle_index.setter
    def work_cycle_index(self, value):
        if value < -len(self.work_cycle):
            self.__work_cycle_index = -1
        else:
            self.__work_cycle_index = value

    def go_back(self, t: int):
        arrived = self.move(t)
        if arrived:
            self.load = 0
            self._destination = self.job.pos
            self.work_cycle_index -= 1

    def work(self, t: int):
        self.load += self.work_speed * t
        print(f'Load of {str(self.job)}:', self.load)
        if self.load >= 10:
            self._destination = self.home.pos
            self.work_cycle_index -= 1

    def go(self, t: int):
        arrived = self.move(t)
        if arrived:
            self.work_cycle_index -= 1

    def set_job(self, item: Union[Mineral, Tree]):
        if isinstance(item, (Mineral, Tree)):
            self.job = item
            self._destination = item.pos

    def actualize(self, surface: pygame.Surface, t):
        if self.job:
            self.work_cycle[self.work_cycle_index](t)
            self.draw(surface)
        else:
            super().actualize(surface, t)

    def is_instantiable(self):
        return True

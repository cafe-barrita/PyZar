import pygame
from vector_2d import Vector
import abc

import cursors
from items import Item


class Character:
    vel_mod = None
    color = None
    radius = 5

    def __init__(self, pos: Vector):
        if self.is_instantiable():
            self.pos = pos
            self._destination = pos
            self._is_pressed = False

    @abc.abstractmethod
    def is_instantiable(self):
        raise TypeError(f'{self.__class__.__name__} is an abstract class and is not instantiable')

    def move(self, t):
        dif = self._destination - self.pos
        if abs(dif) > 1:
            self.pos += dif.unit() * self.vel_mod

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

    # def __init__(self, pos: Vector):
    #     super().__init__(pos)
    #     self.cursors =

    def is_instantiable(self):
        return True

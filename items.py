import pygame
from vector_2d import Vector
import abc

import cursors


class Item:
    vel_mod = None
    color = None

    @abc.abstractmethod
    def is_instantiable(self):
        raise TypeError(f'{self.__class__.__name__} is an abstract class and is not instantiable')

    def __init__(self, pos: Vector):
        if self.is_instantiable():
            self.pos = pos

    def draw(self, surface: pygame.Surface):
        pygame.draw.circle(surface, self.color, self.pos.int(), 5, 0)

    def get_cursor(self):
        return self.cursor


class Tree(Item):
    color = (100, 200, 10)

    def __init__(self, pos: Vector):
        super().__init__(pos)
        self.cursor = (24, 16), (0, 0), *pygame.cursors.compile(cursors.shovel, 'X', '.')

    def is_instantiable(self):
        return True

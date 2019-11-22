import pygame
from vector_2d import Vector
import abc


class Character:
    vel_mod = None
    color = None

    @abc.abstractmethod
    def is_instantiable(self):
        raise TypeError(f'{self.__class__.__name__} is an abstract class and is not instantiable')

    def __init__(self, pos: Vector):
        if self.is_instantiable():
            self.pos = pos
            self.destination = pos

    def move(self, t):
        dif = self.destination - self.pos
        if abs(dif) > 0.1:
            self.pos += dif.unit() * Character.vel_mod

    def draw(self, surface: pygame.Surface):
        pygame.draw.circle(surface, self.color, self.pos.int(), 3, 3)


class Farmer(Character):
    vel_mod = 1
    color = (0, 0, 255)

    def is_instantiable(self):
        return True

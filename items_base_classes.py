from abc import ABC

import pygame
from vector_2d import Vector


class Collective(ABC):
    def __init__(self, collection):
        self.collection = collection

    def screen_move(self, vector: Vector):
        for element in self:
            element._screen_pos += vector

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

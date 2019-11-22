import pygame
from vector_2d import Vector


class Character:
    vel_mod = 1

    def __init__(self, pos: Vector):
        self.pos = pos
        self.destination = pos

    def move(self, t):
        dif = self.destination - self.pos
        if abs(dif) > 0.1:
            self.pos += dif.unit() * Character.vel_mod

    def draw(self, surface: pygame.Surface):
        pygame.draw.circle(surface, (0, 0, 255), self.pos.int(), 3, 3)

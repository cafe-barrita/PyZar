import random

import pygame
from vector_2d import Vector

from perlin import PerlinNoiseFactory


class Sea:
    def __init__(self, res):
        self.pos = Vector(400, 400)
        perlin = PerlinNoiseFactory(2, 3)
        width = int(random.gauss(100, 2))
        height = int(random.gauss(100, 2))
        noise = [[perlin(x / width, y / height) for y in range(height)] for x in range(width)]
        mini = min(min(row) for row in noise)
        noise = [[e + abs(mini) for e in row] for row in noise]
        maxi = max(max(row) for row in noise)
        self.noise = [[int(255 * e / maxi) for e in row] for row in noise]
        print(noise)

    def draw(self, screen, t):
        for x, row in enumerate(self.noise):
            for y, g in enumerate(row):
                pygame.draw.circle(screen, (0, g, 0), (x, y), 1)


if __name__ == '__main__':
    sea = Sea('')

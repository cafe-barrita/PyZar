import pygame
from vector_2d import Vector

from src.perlin import PerlinNoiseFactory

import numpy as np
from skimage import measure


class Terrain:
    def __init__(self, res):
        self.res = res
        perlin = PerlinNoiseFactory(2, 3)
        self.tile_side = 1
        self.noise = [[perlin(x / res[0], y / res[1]) for y in range(0, res[1], self.tile_side)] for x in
                      range(0, res[0], self.tile_side)]
        mini = min(min(row) for row in self.noise)
        noise = [[e + abs(mini) for e in row] for row in self.noise]
        maxi = max(max(row) for row in noise)
        self.noise = [[int(255 * e / maxi) for e in row] for row in noise]
        # threshold = 0.5
        # self.noise = [[1 if e / maxi > threshold else 0 for e in row] for row in noise]
        # TODO meter en un diccionario
        self.isoline = []
        self.calc_contours()

    def calc_contours(self):
        contours = measure.find_contours(self.noise, 150)
        contours = [tuple(e) for e in list(contours[0])]
        self.isoline = [(int(x), int(y)) for x, y in contours]

    def is_contour(self, x, y):
        vector = Vector(x, y)
        adjacents = []
        for dir in self.dirs:
            x, y = (vector + dir).int()
            adjacents.append(self.noise[x][y])
        if not all(adjacents):
            x, y = (vector + self.dirs[adjacents.index(1)]).int()
            if self.noise[x][y]:
                return x, y

    def draw(self, screen, t):
        print(t)
        for x in range(0, self.res[0], self.tile_side):
            for y in range(0, self.res[1], self.tile_side):
                g = self.noise[x // self.tile_side][y // self.tile_side]
                pygame.draw.circle(screen, (0, g, 255 - g), (x, y), self.tile_side)

        pygame.draw.polygon(screen, (200, 0, 0), self.isoline, 1)


if __name__ == '__main__':
    terrain = Terrain('')

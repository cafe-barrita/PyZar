import pygame
from vector_2d import Vector

from perlin import PerlinNoiseFactory

import numpy as np
from skimage import measure
from decorators import kronos


class Terrain:
    @kronos
    def __init__(self, res):
        self.res = res
        perlin = PerlinNoiseFactory(2, 4)
        self.tile_side = 1
        self.noise = np.array([[perlin(x / res[0], y / res[1]) for y in range(0, res[1], self.tile_side)] for x in
                               range(0, res[0], self.tile_side)])
        self.noise -= self.noise.min()
        self.noise *= 255 / self.noise.max()
        # TODO meter en un diccionario
        self.isolines = []
        self.calc_contours()

    def calc_contours(self):
        contours = measure.find_contours(self.noise, 125)
        self.isolines = [[(int(x), int(y)) for x, y in list(contour)] for contour in contours]
        ...

    def draw(self, screen, t):
        print(t)
        for x in range(0, self.res[0], self.tile_side):
            for y in range(0, self.res[1], self.tile_side):
                g = self.noise[x // self.tile_side][y // self.tile_side]
                pygame.draw.circle(screen, (0, g, 255 - g), (x, y), self.tile_side)
                # pygame.draw.circle(screen, (g, g, 255), (x, y), self.tile_side)

        for isoline in self.isolines:
            pygame.draw.polygon(screen, (200, 0, 0), isoline, 1)


if __name__ == '__main__':
    terrain = Terrain('')

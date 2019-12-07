import pygame
from vector_2d import Vector

from items import Item
from perlin import PerlinNoiseFactory

import numpy as np
from skimage import measure
from decorators import kronos


class Terrain(Item):
    def is_instantiable(self):
        return True

    @kronos
    def __init__(self, visible_res, window_pos, pos=Vector(0, 0), res=(int(2e3), int(2e3))):
        # FIXME el terreno debe ser mucho más grande que el mapa visible!!!!!
        super().__init__(pos, window_pos)
        self.res = Vector(*res)
        self.tile = 20
        self.window_pos = Vector(*window_pos)
        self.visible_res = Vector(*visible_res)
        self.sea_threshold = None
        self.perlin = PerlinNoiseFactory(2, 4)
        self.noise_res = self.res / self.tile
        self.noise = np.empty(shape=(self.noise_res.int()))
        self.terrain_set = set()
        self.sea_set = set()
        self.calc_noise()
        # TODO meter en un diccionario
        self.isolines = []
        self.calc_contours(self.window_pos, self.window_pos + self.visible_res)

    @kronos
    def calc_noise(self, ):
        for x in range(int(self.noise_res.x)):
            for y in range(int(self.noise_res.y)):
                noise = self.perlin(x / self.noise_res.x, y / self.noise_res.y)
                self.noise[x, y] = noise
                # if noise < self.sea_threshold:
                #     self.sea_set.add((x, y))
        self.sea_threshold = (self.noise.max() + self.noise.min()) / 2

    def calc_contours(self, v1, v2):
        v1 /= self.tile
        v2 /= self.tile
        v1 = v1.int_vector()
        v2 = v2.int_vector()
        element = self.noise.min()
        noise = self.noise[int(v1.x):int(v2.x), int(v1.y): int(v2.y)]
        noise = np.insert(noise, 0, element, axis=0)
        noise = np.insert(noise, len(noise), element, axis=0)
        noise = np.insert(noise, 0, element, axis=1)
        noise = np.insert(noise, len(noise[1]), element, axis=1)

        self.isolines = [[(int(self.tile * x), int(self.tile * y)) for x, y in list(contour)] for contour in
                         measure.find_contours(noise,
                                               self.sea_threshold, fully_connected='low',
                                               positive_orientation='low')]

    def is_point_inside(self, point):
        return point.int() in self.sea_set

    def draw(self, screen):
        for isoline in self.isolines:
            if len(isoline) > 2:
                pygame.draw.polygon(screen, (0, 0, 200), isoline)

    @kronos
    def screen_move(self, scroll_vector):
        # FIXME hay que mover el sea_set
        self.window_pos -= scroll_vector
        self.calc_contours(self.window_pos, self.window_pos + self.visible_res)

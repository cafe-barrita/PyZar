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
    def __init__(self, visible_res, window_pos, res, pos=Vector(0, 0)):
        # FIXME el terreno debe ser mucho más grande que el mapa visible!!!!!
        super().__init__(pos, window_pos)
        self.res = Vector(*res)
        self.tile = 20
        self.window_pos = Vector(*window_pos)
        self.visible_res = Vector(*visible_res)
        self.sea_threshold = None
        self.perlin = PerlinNoiseFactory(2, 4, tile=(0, 3))
        self.noise_res = self.res / self.tile
        self.noise = np.empty(shape=(self.noise_res.int()))
        self.terrain_set = set()
        self.sea_set = set()
        self.calc_noise()
        self.big_map_isoline = []
        self.mini_map_isoline = []
        # FIXME esto no debería estar hardcodeado
        self.mini_map_pos = None
        self.mini_map_sides = None
        self.calc_contours(self.window_pos, self.window_pos + self.visible_res)

    def set_minimap_data(self, mm_pos, sides):
        self.mini_map_pos = mm_pos
        self.mini_map_sides = sides
        self.calc_contours_for_minimap()

    @kronos
    def calc_noise(self):
        for x in range(int(self.noise_res.x)):
            for y in range(int(self.noise_res.y)):
                noise = self.perlin(x / self.noise_res.x, y / self.noise_res.y)
                self.noise[x, y] = noise
        self.sea_threshold = (self.noise.max() + self.noise.min()) / 2
        for x, col in enumerate(self.noise):
            for y, row in enumerate(col):
                if self.noise[x, y] > self.sea_threshold:
                    self.sea_set.add((x, y))
                else:
                    self.terrain_set.add((x, y))

    def calc_contours_for_minimap(self):
        element = self.noise.min()
        noise = self.noise[:, :]
        noise = np.insert(noise, 0, element, axis=0)
        noise = np.insert(noise, len(noise), element, axis=0)
        noise = np.insert(noise, 0, element, axis=1)
        noise = np.insert(noise, len(noise[1]), element, axis=1)

        isolines = [[(x - 1, y - 1) for x, y in list(contour)] for contour in
                    measure.find_contours(noise, self.sea_threshold, fully_connected='low',
                                          positive_orientation='low')]

        # FIXME this allow the islands, but let spurius lines in between
        if isolines:
            connected_isoline = isolines[0]
            last_element_from_first_line = isolines[0][-1]
            for line in isolines[1:]:
                connected_isoline += line
                connected_isoline.append(last_element_from_first_line)

            self.mini_map_isoline = [(self.mini_map_sides[0] * p[0] / self.noise_res.x + self.mini_map_pos[0],
                                      self.mini_map_sides[1] * p[1] / self.noise_res.y + self.mini_map_pos[1]) for p in
                                     connected_isoline]

    def calc_contours(self, v1, v2):
        v1 /= self.tile
        v2 /= self.tile
        # print(v1, v2)
        element = self.noise.min()
        noise = self.noise[int(v1.x):int(v2.x + 1), int(v1.y): int(v2.y + 1)]
        noise = np.insert(noise, 0, element, axis=0)
        noise = np.insert(noise, len(noise), element, axis=0)
        noise = np.insert(noise, 0, element, axis=1)
        noise = np.insert(noise, len(noise[1]), element, axis=1)

        # isolines = [[(int(self.tile * (x - 1)), int(self.tile * (y - 1))) for x, y in list(contour)] for contour in
        #             measure.find_contours(noise, self.sea_threshold, fully_connected='low',
        #                                   positive_orientation='low')]

        isolines = [[(x - 1, y - 1) for x, y in list(contour)] for contour in
                    measure.find_contours(noise, self.sea_threshold, fully_connected='low',
                                          positive_orientation='low')]

        # FIXME this allow the islands, but let spurius lines in between
        if isolines:
            connected_isoline = isolines[0]
            last_element_from_first_line = isolines[0][-1]
            for line in isolines[1:]:
                connected_isoline += line
                connected_isoline.append(last_element_from_first_line)

            self.big_map_isoline = [(int(self.tile * x), int(self.tile * y)) for x, y in connected_isoline]

    def is_point_inside(self, point):
        point = point / self.tile
        return point.int() in self.sea_set

    def draw(self, screen):
        if self.big_map_isoline:
            pygame.draw.polygon(screen, (0, 0, 200), self.big_map_isoline)

    def draw_for_minimap(self, screen):
        pygame.draw.polygon(screen, (0, 0, 200), self.mini_map_isoline)

    @kronos
    def screen_move(self, window_pos):
        self.window_pos = window_pos
        self.calc_contours(self.window_pos, self.window_pos + self.visible_res)

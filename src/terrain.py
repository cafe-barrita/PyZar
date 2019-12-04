import pygame
from vector_2d import Vector

from items import Item
from perlin import PerlinNoiseFactory

import numpy as np
from skimage import measure
from decorators import kronos


class Terrain(Item):
    @kronos
    def __init__(self, res):
        # FIXME el terreno debe ser mucho más grande que el mapa visible!!!!!
        super().__init__(None)
        self.res = res
        self.sea_threshold = 0.4
        perlin = PerlinNoiseFactory(2, 4)
        # self.noise = np.array([[perlin(x / res[0], y / res[1]) for y in range(res[1])] for x in range(res[0])])
        self.noise = np.empty(shape=res)
        self.sea_dict = {}
        for y in range(res[1]):
            for x in range(res[0]):
                noise = perlin(x / res[0], y / res[1])
                self.noise[x, y] = noise
                if noise < self.sea_threshold:
                    if x not in self.sea_dict:
                        self.sea_dict[x] = {}
                    self.sea_dict[x][y] = 1

        self.noise -= self.noise.min()
        # self.noise *= 255 / self.noise.max()
        self.noise /= self.noise.max()
        # TODO meter en un diccionario
        self.dict_is_corner_x = {0: {0: (0, 0),
                                     self.res[1] - 1: (0, self.res[1] - 1),
                                     },
                                 self.res[0] - 1: {0: (self.res[0] - 1, 0),
                                                   self.res[1] - 1: (self.res[0] - 1, self.res[1] - 1),
                                                   },
                                 }
        self.dict_is_corner_y = {0: {0: (0, 0),
                                     self.res[0] - 1: (self.res[0] - 1, 0),
                                     },
                                 self.res[1] - 1: {0: (0, self.res[1] - 1),
                                                   self.res[0] - 1: (self.res[0] - 1, self.res[1] - 1),
                                                   },
                                 }
        self.isolines = []
        self.low_isolines = []
        self.calc_contours()

    def calc_contours(self):
        # contours = measure.find_contours(self.noise, 90, fully_connected='high', positive_orientation='high')
        # self.isolines = [[(int(x), int(y)) for x, y in list(contour)] for contour in contours]
        self.low_isolines = [[(int(x), int(y)) for x, y in list(contour)] for contour in
                             measure.find_contours(self.noise, self.sea_threshold, fully_connected='low',
                                                   positive_orientation='low')]

        # add corners
        # FIXME it do not add corners if isoline touches oposite sides
        for i, isoline in enumerate(self.low_isolines):
            print(isoline)
            try:
                point = self.dict_is_corner_x[isoline[0][0]][isoline[-1][1]]
            except KeyError:
                try:
                    point = self.dict_is_corner_y[isoline[0][1]][isoline[-1][0]]
                except KeyError:
                    pass
                else:
                    print('RinconY')
                    isoline.append(point)
            else:
                print('RinconX')
                isoline.append(point)

    def is_point_inside(self, point):
        x = point.x
        return x in self.sea_dict and point.y in self.sea_dict[x]

    def draw(self, screen, t, c: bool = True):
        # print(t)
        # for x in range(0, self.res[0], self.tile_side):
        #     for y in range(0, self.res[1], self.tile_side):
        #         g = self.noise[x // self.tile_side][y // self.tile_side]
        #         pygame.draw.circle(screen, (0, g, 255 - g), (x, y), self.tile_side)
        # pygame.draw.circle(screen, (g, g, 255), (x, y), self.tile_side)

        if c:
            # for isoline in self.isolines:
            #     pygame.draw.polygon(screen, (200, 0, 0), isoline, 1)
            for isoline in self.low_isolines:
                # print(isoline[0])
                pygame.draw.polygon(screen, (0, 0, 255), isoline)

    def screen_move(self, scroll_vector):
        self.low_isolines = [[(Vector(*point) + scroll_vector).int() for point in isoline] for isoline in self.low_isolines]


if __name__ == '__main__':
    terrain = Terrain('')

import pygame
from vector_2d import Vector, VectorPolar

from perlin import PerlinNoiseFactory


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
        # self.noise = [[int(255 * e / maxi) for e in row] for row in noise]
        threshold = 0.5
        self.noise = [[e / maxi > threshold for e in row] for row in noise]
        # TODO meter en un diccionario
        self.isoline = []
        self.calc_contours()

    def calc_contours(self):
        angle_increment = 0.78539
        angles = (angle_increment * i for i in range(1, 9))
        dirs = tuple(VectorPolar(1, angle).to_cartesian().int_vector() for angle in angles)
        print(dirs)
        print(self.noise)
        x = 1
        for i, e in enumerate(self.noise[x][:-1]):
            if (e and not self.noise[x][i - 1]) or (e and not self.noise[x][i + 1]):
                self.isoline.append((x, i))
                y = i
                while len(self.isoline) < 2 or self.isoline[0] != self.isoline[-1]:
                    vector = Vector(x, y)
                    for dir in dirs:
                        x, y = (vector + dir).int()
                        if self.noise[x][y]:
                            self.isoline.append((x, y))
                            break

    def draw(self, screen, t):
        print(t)
        # for x in range(0, self.res[0], self.tile_side):
        #     for y in range(0, self.res[1], self.tile_side):
        #         g = self.noise[x // self.tile_side][y // self.tile_side]
        #         pygame.draw.circle(screen, (0, g, 255 - g), (x, y), self.tile_side)

        pygame.draw.polygon(screen, (200, 0, 0), self.isoline, 1)


if __name__ == '__main__':
    terrain = Terrain('')

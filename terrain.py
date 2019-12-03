import pygame

from perlin import PerlinNoiseFactory


class Terrain:
    def __init__(self, res):
        self.res = res
        perlin = PerlinNoiseFactory(2, 3)
        self.tile_side = 4
        self.noise = [[perlin(x / res[0], y / res[1]) for y in range(0, res[1], self.tile_side)] for x in
                      range(0, res[0], self.tile_side)]
        mini = min(min(row) for row in self.noise)
        noise = [[e + abs(mini) for e in row] for row in self.noise]
        maxi = max(max(row) for row in noise)
        self.noise = [[int(255 * e / maxi) for e in row] for row in noise]
        # TODO meter en un diccionario
        self.isoline = []
        # self.calc_coast_line()

    def calc_contours(self):
        # FIXME calcular contornos y dibujar con polyline para que sea más eficiente
        threshold = 0.5

        for x, row in enumerate(self.noise):
            for y, depth in enumerate(row[:-1]):
                if depth >= threshold >= row[y + 1] or depth <= threshold <= row[y + 1]:
                    print(x, y, depth)
                    self.isoline.append((x, y))

    def draw(self, screen, t):
        print(t)
        for x in range(0, self.res[0], self.tile_side):
            for y in range(0, self.res[1], self.tile_side):
                g = self.noise[x // self.tile_side][y // self.tile_side]
                pygame.draw.circle(screen, (0, g, 255 - g), (x, y), self.tile_side)

        # pygame.draw.polygon(screen, (200, 0, 0), self.iso_height_points, 1)


if __name__ == '__main__':
    terrain = Terrain('')

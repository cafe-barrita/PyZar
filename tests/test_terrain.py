import time
import unittest

import pygame

from terrain import Terrain


class MockTerrain(Terrain):
    def __init__(self, res):
        super().__init__(res)
        self.noise = [
            [0, 0, 0, 0, 0],
            [0, 1, 1, 1, 0],
            [0, 0, 1, 1, 0],
            [0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0],
        ]


class TestTerrain(unittest.TestCase):
    def test_contours(self):
        noise = [
            [0, 0, 1, 0, 0],
            [0, 1, 1, 1, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
        ]
        # isoline = ((10, 10), (50, 50), (20, 50))

        # mt = MockTerrain((50, 50))
        # Terrain.calc_contours(mt)

        import numpy as np
        from skimage import measure
        r = np.matrix([
            [0, 0, 0, 0, 0],
            [0, 0, 1, 1, 0],
            [0, 1, 0, 1, 0],
            [0, 1, 1, 1, 0],
            [0, 0, 0, 0, 0],
        ])
        contours = measure.find_contours(r, 0.5)
        contours = [tuple(e) for e in list(contours[0])]
        contours = [(int(x), int(y)) for x, y in contours]
        self.draw(contours)

    def draw(self, isoline):
        pygame.init()
        screen = pygame.display.set_mode((300, 300))
        print(isoline)
        isoline = tuple((x * 30, y * 30) for x, y in isoline)
        pygame.draw.polygon(screen, (255, 0, 0), isoline, 1)
        pygame.display.flip()
        time.sleep(10)

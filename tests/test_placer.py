import unittest

from placer import Placer
from terrain import Terrain


class TestPlacer(unittest.TestCase):
    def test_place_castle(self):
        terrain = Terrain((1000, 1000), (3000, 3000))
        placer = Placer(terrain)
        print(placer.place_castle())

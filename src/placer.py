import math
import random

from vector_2d import Vector, VectorPolar

from terrain import Terrain
from tools import frange


class Placer:
    # FIXME maybe it could be inside terrain class
    instance = None

    def __new__(cls, *args, **kwargs):
        # FIXME maybe it not need to be singleton
        if not Placer.instance:
            Placer.instance = object.__new__(cls)
        return Placer.instance

    def __init__(self, terrain: Terrain):
        self.terrain = terrain

    def place_castle(self):
        # Fixme add timeout
        radius = int(250 / self.terrain.tile)
        alpha = math.atan(1 / radius)
        while 1:
            pos = Vector(random.randrange(radius, self.terrain.noise_res.x - radius),
                         random.randrange(radius, self.terrain.noise_res.y - radius))
            points_set = set(
                (pos + VectorPolar(radius, angle).to_cartesian()).int() for angle in frange(0, 6.29, alpha))
            if points_set.issubset(self.terrain.terrain_set):
                return Vector(*pos) * self.terrain.tile

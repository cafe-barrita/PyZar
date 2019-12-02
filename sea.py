import random

import pygame
from vector_2d import Vector
import math
import pprint


class Sea:
    DIST = 6
    # RADIO = int(DIST / math.sqrt(3))
    RADIO = 3
    CARD = 'nose'
    DIRECTIONS = {
        'n': Vector(0, -DIST),
        'o': Vector(-DIST, 0),
        's': Vector(0, DIST),
        'e': Vector(DIST, 0),
    }

    def __init__(self, resolution):
        self.dict = {key: None for key in random.sample(Sea.CARD, k=4)}
        self.set = set()
        dic = self.dict
        while dic:
            for key in dic:
                dic[key] = {sub_key: None for sub_key in
                            random.sample(Sea.CARD, k=min(4, int(random.gauss(mu=5.5, sigma=1))))}
            dic = dic[key]
        self.clean()

        # pprint.pprint(self.dict)

    def clean(self):
        dic = self.dict
        vector = Vector(400, 400)
        self.set.add(vector)
        while dic:
            for key in dic:
                vector += Sea.DIRECTIONS[key]
                self.set.add(vector)
            dic = dic[key]

    def draw(self, surface, t):
        print(t)
        for vector in self.set:
            pygame.draw.circle(surface, (0, 50, 255), vector.int(), Sea.RADIO)

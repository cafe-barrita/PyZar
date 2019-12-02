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
        'p': Vector(0, 0),
    }

    def __init__(self, resolution):
        # self.dict = {key: None for key in random.sample(Sea.CARD, k=4)}
        # self.set = set()
        # dic = self.dict
        # while dic:
        #     for key in dic:
        #         dic[key] = {sub_key: None for sub_key in
        #                     random.sample(Sea.CARD, k=min(4, int(random.gauss(mu=5.5, sigma=1))))}
        #     dic = dic[key]
        # self.clean()

        # pprint.pprint(self.dict)

        CARD = ('n', 'o', 's', 'e', 'p')
        output = {'n', 'o', 's', 'e'}
        for _ in range(20):
            output_copy = output.copy()
            for element in output_copy:
                if element[-1] != 'p':
                    output.discard(element)
                    for element2 in random.sample(CARD, k=max(0, min(4, int(random.gauss(mu=2.6, sigma=1))))):
                        output.add(element + element2)
        print(output)
        self.output = output
        self.vector_set = set()
        self.clean()

    def clean(self):
        # dic = self.dict
        # vector = Vector(400, 400)
        # self.set.add(vector)
        # while dic:
        #     for key in dic:
        #         vector += Sea.DIRECTIONS[key]
        #         self.set.add(vector)
        #     dic = dic[key]
        vector = Vector(400, 400)
        vector_set = {vector}
        for element in self.output:
            vector = Vector(400, 400)
            for letter in element:
                vector += Sea.DIRECTIONS[letter]
                vector_set.add(vector)

        self.vector_set = vector_set
        print(vector_set)

    def draw(self, surface, t):
        print(t)
        for vector in self.vector_set:
            pygame.draw.circle(surface, (0, 50, 255), vector.int(), Sea.RADIO)


if __name__ == '__main__':
    CARD = ('n', 'o', 's', 'e', 'p')
    output = {'n', 'o', 's', 'e'}
    for _ in range(4):
        output_copy = output.copy()
        for element in output_copy:
            if element[-1] != 'p':
                output.discard(element)
                for element2 in random.sample(CARD, k=random.randrange(6)):
                    output.add(element + element2)
    print(output)

    vector = Vector(400, 400)
    vector_set = {vector}
    for element in output:
        for letter in element:
            vector += Sea.DIRECTIONS[letter]
            vector_set.add(vector)

    print(vector_set)

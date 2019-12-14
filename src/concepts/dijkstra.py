import asyncio
from dataclasses import dataclass
from typing import List

import pygame
from vector_2d import VectorPolar, Vector

from tools import kronos


class Path:
    vectors_weights_tuple = (
        (Vector(1, 0), 1), (Vector(1, 1), 1.4), (Vector(0, 1), 1), (Vector(-1, 1), 1.4), (Vector(-1, 0), 1),
        (Vector(-1, -1), 1.4), (Vector(0, -1), 1), (Vector(1, -1), 1.4))

    def __init__(self):
        self.points = []
        self.show_points = []
        self.tile = 20
        self.sea_set = {(x, 12) for x in range(5, 25)}
        self.sea_set.update({(12, y) for y in range(5, 25)})

        self.sea_set.update({(35, y) for y in range(5, 25)})
        self.sea_set.update({(55, y) for y in range(5, 25)})
        self.sea_set.update({(x, 25) for x in range(35, 56)})
        self.sea_set.update({(x, 5) for x in range(37, 56)})
        self.sea_set.update({(37, y) for y in range(5, 23)})
        self.sea_set.update({(52, y) for y in range(8, 23)})
        self.sea_set.update({(x, 23) for x in range(37, 53)})

        self.show_sea = [(self.tile * x, self.tile * y) for x, y in self.sea_set]
        self.intermediate_points = [(Vector(), 1)]

    def draw(self, screen):
        for point in self.show_sea:
            pygame.draw.circle(screen, (0, 0, 255), point, 4)

        max_weight = max(self.intermediate_points, key=lambda tup: tup[1])[1]
        for point, weight in self.intermediate_points:
            pygame.draw.circle(screen, (weight * 255 / max_weight, 0, 0), point.int(), 3)

        for point in self.show_points:
            pygame.draw.circle(screen, (0, 255, 0), point.int(), 2)

    @kronos
    def get_dijkstra(self, source: Vector, destination: Vector):
        pos = (source / self.tile).int_vector()
        destination = (destination / self.tile).int_vector()
        dijkstra_nodes = {pos: (1, [])}
        while destination not in dijkstra_nodes:
            dijkstra_nodes_copy = dijkstra_nodes.copy()
            for node, (weight, path) in dijkstra_nodes_copy.items():
                for adjacent, step_weight in self.get_adjacents(node):
                    adjacent_weight = weight + step_weight
                    adjacent_path = path + [node]
                    if adjacent in dijkstra_nodes:
                        if dijkstra_nodes[adjacent][0] > adjacent_weight:
                            dijkstra_nodes[adjacent] = (adjacent_weight, adjacent_path)
                    else:
                        dijkstra_nodes[adjacent] = (adjacent_weight, adjacent_path)

        self.intermediate_points = [(point * self.tile, value[0]) for point, value in
                                    dijkstra_nodes.items()]

        self.points = [destination] + list(reversed(dijkstra_nodes[destination][1]))
        self.show_points = [self.tile * point for point in self.points]
        print(self.points)

    def get_adjacents(self, node):
        for vector, weight in Path.vectors_weights_tuple:
            next_node = node + vector
            if next_node.int() not in self.sea_set:
                yield next_node, weight

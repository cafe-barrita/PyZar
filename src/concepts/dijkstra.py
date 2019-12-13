import asyncio
from typing import List

import pygame
from vector_2d import VectorPolar, Vector


class Path:
    def __init__(self, res):
        self.points = []
        self.show_points = []
        self.tile = 10
        self.sea_set = set()
        self.show_sea = [10 * point for point in self.sea_set]
        self.intermediate_points = [(Vector(), 1)]

    def draw(self, screen):
        max_weight = max(self.intermediate_points, key=lambda tup: tup[1])[1]
        for point, weight in self.intermediate_points:
            pygame.draw.circle(screen, (weight * 255 / max_weight, 0, 0), point.int(), 3)

        for point in self.show_points:
            pygame.draw.circle(screen, (0, 255, 0), point.int(), 3)

    def get_dijkstra(self, source: Vector, destination: Vector):
        pos = (source / self.tile).int_vector()
        destination = (destination / self.tile).int_vector()
        dijkstra_nodes = {pos: (1, [])}
        while destination not in dijkstra_nodes:
            dijkstra_nodes_copy = dijkstra_nodes.copy()
            for node, value in dijkstra_nodes_copy.items():
                weight, path = value
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
        # await asyncio.sleep(0.0001)

        self.points = [destination] + [point for point in reversed(dijkstra_nodes[destination][1])]
        self.show_points = [10 * point for point in self.points]
        print(dijkstra_nodes[destination][1])
        print(self.show_points)
        # return [destination * self.tile] + [point * self.tile for point in reversed(dijkstra_nodes[destination][1])]

    def get_adjacents(self, node):
        alpha = 0.79
        for i in range(8):
            weight = 1 if i % 2 == 0 else 1.4
            weight *= 999 if node.int() in self.sea_set else 1
            yield node + VectorPolar(1, alpha * i).to_cartesian().int_vector(), weight

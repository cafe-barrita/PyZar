import random
import time
from abc import ABC
from collections import deque
from typing import Union, Deque, List

import pygame
from vector_2d import Vector, VectorPolar

import cursors
from items import Item, Mineral, Tree, Building, Forest, RoundItem, Castle, Collective
from terrain import Terrain
from tools import frange


class Character(RoundItem, ABC):
    vel_mod = None
    cursors = None
    radius = 5
    sight_radius = 50

    def __init__(self, pos: Vector, terrain: Terrain):
        super().__init__(pos)
        self.terrain = terrain
        self.__destinations: Deque[Vector, ...] = deque([pos])
        self.__intermediate_destinations = []
        self._is_pressed = False
        self.obstacle = None
        self.dijkstra_nodes = {}
        self._dest_screen_pos = []

    @property
    def director_vector(self):
        # todo meybe unit vector * radius
        if self.destination:
            return (self.destination - self._pos).unit()
        else:
            return Vector()

    @property
    def intermediate_destinations(self):
        raise NotImplementedError

    @intermediate_destinations.setter
    def intermediate_destinations(self, value):
        self.__intermediate_destinations.append(value)

    @property
    def destination(self) -> Vector:
        if not self.__intermediate_destinations:
            if not self.__destinations:
                return None
            destination = self.__destinations.pop()
            self.__intermediate_destinations += self.get_dijkstra(destination)
            self.dijkstra_nodes = {}
            # print(self.__intermediate_destinations)
        return self.__intermediate_destinations[-1]

    @destination.setter
    def destination(self, value: Vector):
        self.__destinations.append(value)

    def destinations_pop(self):
        self.__intermediate_destinations.pop()

    @staticmethod
    def get_new_unit_vectors(pos):
        angle_step = 0.7854  # pi/4
        return (pos + VectorPolar(1, angle).to_cartesian() for angle in frange(0, 6.29, angle_step))

    def append_left_destination(self, value):
        self.__destinations.appendleft(value)

    def move(self, t: int) -> bool:
        destination = self.destination
        if destination:
            if abs(destination - self._pos) > self.radius:
                movement = self.director_vector * self.vel_mod * t
                self._pos += movement
                self._screen_pos += movement
                return False
            else:
                self.destinations_pop()
                return True

    def screen_move(self, window_pos):
        super().screen_move(window_pos)
        self._dest_screen_pos = [dest - window_pos for dest in self.__intermediate_destinations]

    def draw(self, surface: pygame.Surface):
        pygame.draw.circle(surface, self.color, self._screen_pos.int(), self.radius, 0)
        if self._is_pressed:
            pygame.draw.circle(surface, (0, 255, 0), self._screen_pos.int(), self.radius, 1)

        # for point, value in self.dijkstra_nodes.items():
        #     (value[0] / 30) * 255
        #     pygame.draw.circle(surface, ((value[0] / 999) * 200, 0, 0), (self._screen_pos + point).int(), 3)

        # for dest in self._destinations:
        #     pygame.draw.circle(surface, (255, 0, 0), dest.int(), 1, 1)
        for dest in self._dest_screen_pos:
            print('DEST:', dest)
            pygame.draw.circle(surface, (255, 0, 0), dest.int(), 3)

    def actualize(self, surface: pygame.Surface, t: int):
        self.move(t)
        self.draw(surface)

    def set_pressed(self, value: bool):
        self._is_pressed = value

    def get_cursor(self, item: Item):
        return self.cursors.get(item.__class__.__name__, pygame.cursors.arrow)

    def get_dijkstra(self, destination: Vector) -> List[Vector]:
        pos = (self._pos / self.terrain.tile).int_vector()
        # print('POS:', self._pos)
        destination = (destination / self.terrain.tile).int_vector()
        if pos not in self.dijkstra_nodes:
            self.dijkstra_nodes[pos] = (0, [])
        while destination not in self.dijkstra_nodes:
            # print(self.dijkstra_nodes)
            # time.sleep(1)
            dijkstra_nodes_copy = self.dijkstra_nodes.copy()
            for node, value in dijkstra_nodes_copy.items():
                weight, path = value
                # adjacents = self.get_adjacents(node)
                for adjacent, step_weight in self.get_adjacents(node):
                    adjacent_weight = weight + step_weight
                    adjacent_path = path + [node]
                    if adjacent in self.dijkstra_nodes:
                        if self.dijkstra_nodes[adjacent][0] > adjacent_weight:
                            self.dijkstra_nodes[adjacent] = (adjacent_weight, adjacent_path)
                    else:
                        self.dijkstra_nodes[adjacent] = (adjacent_weight, adjacent_path)

        return [destination * self.terrain.tile] + [point * self.terrain.tile for point in reversed(self.dijkstra_nodes[destination][1])]

    # def get_dijkstra_step(self, destination):
    #     pos = (self._pos / self.terrain.tile).int_vector()
    #     if pos not in self.dijkstra_nodes:
    #         self.dijkstra_nodes[pos] = (0, [])
    #     dijkstra_nodes_copy = self.dijkstra_nodes.copy()
    #     for node, value in dijkstra_nodes_copy.items():
    #         weight, path = value
    #         # adjacents = self.get_adjacents(node)
    #         for adjacent, step_weight in self.get_adjacents(node):
    #             adjacent_weight = weight + step_weight
    #             sdjacent_path = path + [node]
    #             if adjacent in self.dijkstra_nodes:
    #                 if self.dijkstra_nodes[adjacent][0] > adjacent_weight:
    #                     self.dijkstra_nodes[adjacent] = (adjacent_weight, sdjacent_path)
    #             else:
    #                 self.dijkstra_nodes[adjacent] = (adjacent_weight, sdjacent_path)
    #
    #     return [destination]

    # @staticmethod
    def get_adjacents(self, node):
        # node = (node / self.terrain.tile).int_vector()
        alpha = 0.79
        for i in range(8):
            weight = 1 if i % 2 == 0 else 1.4
            weight *= 999 if node.int() in self.terrain.sea_set else 1
            yield node + VectorPolar(1, alpha * i).to_cartesian().int_vector(), weight

            # points_set = set(
            #     (pos + VectorPolar(radius, angle).to_cartesian()).int() for angle in frange(0, 6.29, alpha))
            # if points_set.issubset(self.terrain.terrain_set):
            #     return Vector(*pos) * self.terrain.tile


class Farmer(Character):
    vel_mod = 0.05
    color = 0, 0, 255
    cursors = {'Tree': cursors.compiled_axe,
               'Building': cursors.compiled_shovel,
               'Mineral': cursors.compiled_pick,
               }
    radius = 10
    UNEMPLOYED = 'unemployed'
    CHOPPER = 'chopper'
    MINER = 'miner'

    def __init__(self, pos: Vector, home: Building, forest: Forest, terrain: Terrain):
        super().__init__(pos, terrain)
        self.work_cycle = [self.get_back_from_work, self.work, self.go_to_work]
        self.__work_cycle_index = -1
        self.job = None
        self.load = 0
        self.work_speed = 0.01
        self.home = home
        self.status = Farmer.UNEMPLOYED
        self.forest = forest

    @property
    def work_cycle_index(self):
        return self.__work_cycle_index

    @work_cycle_index.setter
    def work_cycle_index(self, value):
        if value < -len(self.work_cycle):
            self.__work_cycle_index = -1
        else:
            self.__work_cycle_index = value

    def get_back_from_work(self, t: int):
        if self.move(t):
            # if self.home.is_point_inside(self._pos + self.director_vector.unit() * self.radius * 2):
            self.load = 0
            # self.destination = None
            self.destination = self.job
            self.work_cycle_index -= 1

    def work(self, t: int):
        self.load += self.work_speed * t
        if self.load >= 10:
            self.job.has_been_worked()
            if not self.job.is_alive():
                if isinstance(self.job, Tree):
                    self.forest.discard(self.job)
                self.job = None
            self.destination = self.home
            self.work_cycle_index -= 1

    def go_to_work(self, t: int):
        if self.move(t):
            self.work_cycle_index -= 1

    def set_job(self, item: Union[Mineral, Tree]):
        self.job = item
        self.destination = item
        if isinstance(item, Tree):
            self.status = Farmer.CHOPPER
        if isinstance(item, Mineral):
            self.status = Farmer.MINER

    def actualize(self, surface: pygame.Surface, t):
        if self.job:
            self.work_cycle[self.work_cycle_index](t)
            self.draw(surface)
        elif self.status == Farmer.CHOPPER:
            for tree in self.forest:
                # FIXME que sea el más cercano
                if abs(tree.pos - self._pos) < 100:
                    self.job = tree
                    return
            self.status = Farmer.UNEMPLOYED
            self.__work_cycle_index = -1

        else:
            super().actualize(surface, t)

    def is_instantiable(self):
        return True

    # def draw(self, screen):
    #     super().draw(screen)


class Characters(Collective):
    def __init__(self, castle: Castle, forest: Forest, terrain: Terrain):
        farmers = [Farmer((castle.pos.to_polar() + VectorPolar(50, random.randrange(628) // 100)).to_cartesian(),
                          home=castle, forest=forest, terrain=terrain) for _ in range(3)]
        super().__init__(farmers)

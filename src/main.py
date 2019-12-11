import collections
import os
import sys
from typing import Optional

import pygame
from pygame.rect import Rect
from vector_2d import Vector

from characters import Character, Characters
from interactions import Interaction
from items import Mineral, Castle, Forest, Borders
from terrain import Terrain

EVERY_SECOND_EVENT = 31


class Window:
    def __init__(self, pos, res, map_res):
        self.__pos = Vector(*pos)
        self.res = Vector(*res)
        self.__map_res = Vector(*map_res)

    @property
    def pos(self):
        return self.__pos

    @pos.setter
    def pos(self, value):
        self.__pos = value

    def move(self, scroll_vector: Vector):
        pos = self.__pos - scroll_vector
        bottom_right = pos + self.res
        if pos.x >= 0 and pos.y >= 0 and bottom_right.x < self.__map_res.x and bottom_right.y < self.__map_res.y:
            self.__pos = pos
            return True
        return False


class MiniMap:
    def __init__(self, window, map_res, terrain, stuff):
        self.window_size = window.res.x / map_res[0], window.res.y / map_res[1]
        self.factor = 10
        self.margin = 10
        sides = Vector(*map_res) / self.factor
        self.pos = Vector(self.margin, screen_resolution[1] - self.margin - sides[1])
        self.center = self.pos - sides / 2
        self.window_points = (
            self.pos,
            self.pos + Vector(window.res.x, 0) / self.factor,
            self.pos + window.res / self.factor,
            self.pos + Vector(0, window.res.y) / self.factor,
        )
        self.window_tuples = tuple((p + window.pos / self.factor).int() for p in self.window_points)
        self.points = (
            (self.margin - 1, window.res.y - self.margin + 1),
            (self.margin + sides.x + 1, window.res.y - self.margin + 1),
            (self.margin + sides.x + 1, window.res.y - self.margin - sides.y - 1),
            (self.margin - 1, window.res.y - self.margin - sides.y - 1),
        )
        xs = [int(point[0]) for point in self.points]
        ys = [int(point[1]) for point in self.points]
        self.x_bounds = min(xs), max(xs)
        self.y_bounds = min(ys), max(ys)
        self.terrain = terrain
        terrain.set_minimap_data(self.pos, sides)
        self.stuff = stuff

    def click(self, point: Vector):
        if self.x_bounds[1] >= point.x >= self.x_bounds[0] and self.y_bounds[1] >= point.y >= self.y_bounds[0]:
            point = (point - self.pos) * self.factor
            # print('CLICK', point)
            self.screen_move(point)
            return point

    def draw(self, screen):
        pygame.draw.polygon(screen, (0, 0, 0), self.points)
        self.terrain.draw_for_minimap(screen)
        pygame.draw.polygon(screen, (255, 255, 0), self.points, 3)
        pygame.draw.polygon(screen, (200, 255, 0), self.window_tuples, 2)

    def screen_move(self, window_pos):
        self.window_tuples = tuple((p + window_pos / self.factor).int() for p in self.window_points)


def do_each_second():
    Interaction.check_obstacles(characters, obstacles + characters)
    Interaction.check_sea(characters, terrain)


if sys.platform == 'win32' or sys.platform == 'win64':
    os.environ['SDL_VIDEO_CENTERED'] = '1'

pygame.init()
screen_resolution = 1200, 800
map_resolution = int(2e3), int(2e3)
pygame.display.set_caption('PyZar')
screen = pygame.display.set_mode(screen_resolution)
clock = pygame.time.Clock()
t = clock.get_time()
done = False
noir = 0, 0, 0
fps = 60
fps_to_show = collections.deque([60] * 60)

borders = Borders(screen_resolution)
window = Window(pos=(400, 300), res=screen_resolution, map_res=map_resolution)
terrain = Terrain(screen_resolution, window.pos, map_resolution)
castle = Castle(Vector(400, 300), window.pos)
pressed_one: Optional[Character] = None
mineral = Mineral(Vector(300, 100), window.pos)
mineral2 = Mineral(Vector(500, 100), window.pos)
obstacles = [castle, mineral, mineral2]
forest = Forest(map_resolution, obstacles + [terrain], window.pos)
characters = Characters(castle, forest, window.pos)
mini_map = MiniMap(window, map_resolution, terrain, (castle, mineral, mineral2, characters))

pygame.time.set_timer(EVERY_SECOND_EVENT, 200)
font = pygame.font.Font('freesansbold.ttf', 20)
text = font.render('XX.X FPS', True, (255, 0, 0), (0, 0, 255))
text_rect: Rect = text.get_rect()
text_rect.bottomright = (screen_resolution[0] - 10, screen_resolution[1] - 20)
while not done:
    screen.fill(noir)
    terrain.draw(screen)
    castle.draw(screen)
    forest.draw(screen)
    mineral.draw(screen)
    mineral2.draw(screen)
    characters.actualize(screen, t)
    mini_map.draw(screen)
    screen.blit(text, text_rect)

    mouse_vector = Vector(*pygame.mouse.get_pos()) + window.pos
    scroll_vector = borders.get_hovered(Vector(*pygame.mouse.get_pos()))
    for event in pygame.event.get():
        if event.type == pygame.MOUSEMOTION:
            # print('mouse', pygame.mouse.get_pos())
            # print('mouse on map', mouse_vector)
            # print('window', window.pos)
            # print()
            # mouse_peq = mouse_vector / terrain.tile
            # print(terrain.sea_threshold, terrain.noise[int(mouse_peq[0]), int(mouse_peq[1])])
            if pressed_one:
                hovered = Interaction.get_hovered(mouse_vector, forest + obstacles)
                if hovered:
                    pygame.mouse.set_cursor(*pressed_one.get_cursor(hovered))
                else:
                    pygame.mouse.set_cursor(*pygame.cursors.arrow)
            else:
                pygame.mouse.set_cursor(*pygame.cursors.arrow)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                point = mini_map.click(Vector(*pygame.mouse.get_pos()))
                if point:
                    window.pos = point
                    scroll_vector = Vector(0, 0)
                pressed_item = Interaction.get_hovered(mouse_vector, forest + obstacles)
                print(mouse_vector)
                if pressed_item and pressed_one:
                    pressed_one.set_job(pressed_item)
                pressed_one = Interaction.mouse_characters(mouse_vector, characters)
            elif event.button == 3 and pressed_one:
                pressed_one.append_left_destination(mouse_vector)
            # elif event.button == 4:
            #     ...
            # elif event.button == 5:
            #     ...
        elif event.type == EVERY_SECOND_EVENT:
            do_each_second()

        elif event.type == pygame.QUIT:
            done = True

    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_w]:
        scroll_vector = Vector(0, 1)
    elif teclas[pygame.K_a]:
        scroll_vector = Vector(1, 0)
    elif teclas[pygame.K_s]:
        scroll_vector = Vector(0, -1)
    elif teclas[pygame.K_d]:
        scroll_vector = Vector(-1, 0)
    if scroll_vector and pygame.mouse.get_focused() and window.move(scroll_vector):
        forest.screen_move(window.pos)
        characters.screen_move(window.pos)
        terrain.screen_move(window.pos)
        mini_map.screen_move(window.pos)
        for obstacle in obstacles:
            obstacle.screen_move(window.pos)

    # if teclas[pygame.K_KP_MINUS]:
    #     ...

    # para sair
    if teclas[pygame.K_ESCAPE]:
        done = True

    t = clock.get_time()
    if t != 0:
        fps_to_show.popleft()
        fps_to_show.append(1000 / t)
    text = font.render(f'{round(sum(fps_to_show) / len(fps_to_show), 1)} FPS', True, (255, 255, 0), (0, 0, 0))

    pygame.display.flip()

    clock.tick(fps)

pygame.quit()

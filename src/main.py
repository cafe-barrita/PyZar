import collections
import os
import sys
from typing import Optional

import pygame
from pygame.rect import Rect
from vector_2d import Vector

from characters import Character, Characters
from gui import Window, MiniMap
from interactions import Interaction
from items import Mineral, Castle, Forest, Borders
from terrain import Terrain

EVERY_SECOND_EVENT = 31


def do_each_second():
    Interaction.check_obstacles(characters, obstacles + characters)
    Interaction.check_sea(characters, terrain)


if sys.platform == 'win32' or sys.platform == 'win64':
    os.environ['SDL_VIDEO_CENTERED'] = '1'

pygame.init()
screen_resolution = 1200, 800
side = 2e3
map_resolution = int(side), int(side)
pygame.display.set_caption('PyZar')
screen = pygame.display.set_mode(screen_resolution)
clock = pygame.time.Clock()
t = clock.get_time()
done = False
noir = 0, 0, 0
fps = 200
fps_to_show = collections.deque([60] * 60)

borders = Borders(screen_resolution)
terrain = Terrain(screen_resolution, map_resolution)
castle = Castle(Vector(400, 300))
pressed_one: Optional[Character] = None
mineral = Mineral(Vector(300, 100))
mineral2 = Mineral(Vector(500, 100))
obstacles = [castle, mineral, mineral2]
forest = Forest(map_resolution, obstacles + [terrain])
characters = Characters(castle, forest)
window = Window(center=castle.pos, res=screen_resolution, map_res=map_resolution)
mini_map = MiniMap(window, map_resolution, terrain, (castle, mineral, mineral2, characters))

pygame.time.set_timer(EVERY_SECOND_EVENT, 200)
font = pygame.font.Font('freesansbold.ttf', 20)
text = font.render('XX.X FPS', True, (255, 0, 0), (0, 0, 255))
text_rect: Rect = text.get_rect()
text_rect.bottomright = (screen_resolution[0] - 10, screen_resolution[1] - 20)

# A function would look prettier but it is much slower
forest.screen_move(window.pos)
characters.screen_move(window.pos)
terrain.screen_move(window.pos)
mini_map.screen_move(window.pos)
for obstacle in obstacles:
    obstacle.screen_move(window.pos)

while not done:
    mouse = Vector(*pygame.mouse.get_pos())
    mouse_in_map = mouse + window.pos
    scroll_vector = borders.get_hovered(mouse)
    for event in pygame.event.get():
        if event.type == pygame.MOUSEMOTION:
            if pygame.mouse.get_pressed()[0]:
                scroll_vector = mini_map.click(mouse)
            if pressed_one:
                hovered = Interaction.get_hovered(mouse_in_map, forest + obstacles)
                if hovered:
                    pygame.mouse.set_cursor(*pressed_one.get_cursor(hovered))
                else:
                    pygame.mouse.set_cursor(*pygame.cursors.arrow)
            else:
                pygame.mouse.set_cursor(*pygame.cursors.arrow)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                scroll_vector = mini_map.click(mouse)
                pressed_item = Interaction.get_hovered(mouse_in_map, forest + obstacles)
                if pressed_item and pressed_one:
                    pressed_one.set_job(pressed_item)
                pressed_one = Interaction.mouse_characters(mouse_in_map, characters)
            elif event.button == 3 and pressed_one:
                pressed_one.append_left_destination(mouse_in_map)
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
        # A function would look prettier but it is much slower
        forest.screen_move(window.pos)
        characters.screen_move(window.pos)
        terrain.screen_move(window.pos)
        mini_map.screen_move(window.pos)
        for obstacle in obstacles:
            obstacle.screen_move(window.pos)

    if teclas[pygame.K_ESCAPE]:
        done = True

    t = clock.get_time()
    if t != 0:
        fps_to_show.popleft()
        fps_to_show.append(1000 / t)
    text = font.render(f'{round(sum(fps_to_show) / len(fps_to_show), 1)} FPS', True, (255, 255, 0), (0, 0, 0))

    screen.fill(noir)
    terrain.draw(screen)
    castle.draw(screen)
    forest.draw(screen)
    mineral.draw(screen)
    mineral2.draw(screen)
    characters.actualize(screen, t)
    mini_map.draw(screen)
    screen.blit(text, text_rect)
    pygame.display.flip()

    clock.tick(fps)

pygame.quit()

import os
import sys
from typing import Optional

import pygame
from vector_2d import Vector

from characters import Character, Characters
from interactions import Interaction
from items import Mineral, Castle, Forest, Borders, Tree
from terrain import Terrain

EVERY_SECOND_EVENT = 31


def do_each_second():
    Interaction.check_obstacles(characters, obstacles + characters)
    # Interaction.check_sea(characters, terrain)


if sys.platform == 'win32' or sys.platform == 'win64':
    os.environ['SDL_VIDEO_CENTERED'] = '1'

pygame.init()
resolution = 1200, 800
pygame.display.set_caption('PyZar')
screen = pygame.display.set_mode(resolution)
clock = pygame.time.Clock()
t = clock.get_time()
done = False
noir = 0, 0, 0
fps = 60

borders = Borders(resolution)
window_pos = Vector(400, 300)
terrain = Terrain(resolution, window_pos)
castle = Castle(Vector(400, 300), window_pos)
pressed_one: Optional[Character] = None
mineral = Mineral(Vector(300, 100), window_pos)
mineral2 = Mineral(Vector(500, 100), window_pos)
obstacles = [castle, mineral, mineral2]
forest = Forest(resolution, obstacles, window_pos)
characters = Characters(castle, forest, window_pos)
# tree = Tree(Vector(400, 300), window_pos)
# tree.color = (255, 255, 0)
# tree.radius = 500

pygame.time.set_timer(EVERY_SECOND_EVENT, 200)
while not done:
    screen.fill(noir)
    castle.draw(screen)
    forest.draw(screen)
    mineral.draw(screen)
    mineral2.draw(screen)
    # tree.draw(screen)
    terrain.draw(screen)
    characters.actualize(screen, t)
    mouse_vector = Vector(*pygame.mouse.get_pos()) + window_pos
    scroll_vector = borders.get_hovered(Vector(*pygame.mouse.get_pos()))
    # mouse_vector -= total_scroll_vector
    for event in pygame.event.get():
        if event.type == pygame.MOUSEMOTION:
            # print('mouse', pygame.mouse.get_pos())
            # print('mouse on map', mouse_vector)
            # print('window', window_pos)
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
    if scroll_vector and pygame.mouse.get_focused():
        window_pos -= scroll_vector
        forest.screen_move(scroll_vector)
        # tree.screen_move(scroll_vector)
        characters.screen_move(scroll_vector)
        terrain.screen_move(scroll_vector)
        for obstacle in obstacles:
            obstacle.screen_move(scroll_vector)

    # if teclas[pygame.K_KP_MINUS]:
    #     ...

    # para sair
    if teclas[pygame.K_ESCAPE]:
        done = True

    t = clock.get_time()

    pygame.display.flip()

    clock.tick(fps)

pygame.quit()

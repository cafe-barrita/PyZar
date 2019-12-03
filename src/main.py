import os
import sys
from typing import Optional

import pygame
from vector_2d import Vector, VectorPolar

from characters import Character, Characters
from interactions import Interaction
from items import Mineral, Castle, Forest, Borders

EVERY_SECOND_EVENT = 31


def do_each_second():
    Interaction.check_obstacles(characters, obstacles + characters)


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
fps = 20

borders = Borders(resolution)
castle = Castle(Vector(400, 300))
pressed_one: Optional[Character] = None
mineral = Mineral(Vector(300, 100))
mineral2 = Mineral(Vector(500, 100))
obstacles = [castle, mineral, mineral2]
forest = Forest(resolution, obstacles)
characters = Characters(castle, forest)

pygame.time.set_timer(EVERY_SECOND_EVENT, 200)
total_scroll_vector = Vector()
while not done:
    screen.fill(noir)
    castle.draw(screen)
    forest.draw(screen)
    mineral.draw(screen)
    mineral2.draw(screen)
    characters.actualize(screen, t)
    mouse_vector = Vector(*pygame.mouse.get_pos())
    scroll_vector = borders.get_hovered(mouse_vector)
    mouse_vector -= total_scroll_vector
    for event in pygame.event.get():
        if event.type == pygame.MOUSEMOTION:
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
    if scroll_vector:
        scroll_vector *= 5
        total_scroll_vector += scroll_vector
        forest.screen_move(scroll_vector)
        characters.screen_move(scroll_vector)
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

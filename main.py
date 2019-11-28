import os
import random
import sys
from typing import Optional

import pygame
from vector_2d import Vector, VectorPolar

from characters import Farmer, Character
from interactions import Interaction
from items import Mineral, Castle, Forest

EVERY_SECOND_EVENT = 31


def do_each_second():
    Interaction.check_obstacles(farmers, [mineral, mineral2, castle] + farmers)


if sys.platform == 'win32' or sys.platform == 'win64':
    os.environ['SDL_VIDEO_CENTERED'] = '1'

pygame.init()
resolution = 800, 600
pygame.display.set_caption('PyZar')
screen = pygame.display.set_mode(resolution)
clock = pygame.time.Clock()
t = clock.get_time()
done = False
noir = 0, 0, 0
fps = 20

castle = Castle(Vector(400, 300))
forest = Forest(resolution)
farmers = [Farmer((castle.pos.to_polar() + VectorPolar(50, random.randrange(628) // 100)).to_cartesian(),
                  home=castle,
                  forest=forest) for _ in range(3)]
pressed_one: Optional[Character] = None
mineral = Mineral(Vector(300, 100))
mineral2 = Mineral(Vector(500, 100))

pygame.time.set_timer(EVERY_SECOND_EVENT, 200)

while not done:
    screen.fill(noir)
    castle.draw(screen)
    forest.draw(screen)
    mineral.draw(screen)
    mineral2.draw(screen)
    for farmer in farmers:
        farmer.actualize(screen, t)

    for event in pygame.event.get():
        if event.type == pygame.MOUSEMOTION:
            if pressed_one:
                hovered = Interaction.get_hovered(Vector(*pygame.mouse.get_pos()),
                                                  forest.tree_set.union([mineral, mineral2]))
                if hovered:
                    pygame.mouse.set_cursor(*pressed_one.get_cursor(hovered))
                else:
                    pygame.mouse.set_cursor(*pygame.cursors.arrow)
            else:
                pygame.mouse.set_cursor(*pygame.cursors.arrow)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                pressed_item = Interaction.get_hovered(Vector(*pygame.mouse.get_pos()),
                                                       forest.tree_set.union([mineral, mineral2]))
                if pressed_item and pressed_one:
                    pressed_one.set_job(pressed_item)
                pressed_one = Interaction.mouse_characters(Vector(*pygame.mouse.get_pos()), farmers)
            elif event.button == 3 and pressed_one:
                pressed_one.append_left_destination(Vector(*pygame.mouse.get_pos()))
            # elif event.button == 4:
            #     ...
            # elif event.button == 5:
            #     ...
        elif event.type == EVERY_SECOND_EVENT:
            do_each_second()

        elif event.type == pygame.QUIT:
            done = True

    teclas = pygame.key.get_pressed()
    # if teclas[pygame.K_KP_PLUS]:
    #     ...
    # if teclas[pygame.K_KP_MINUS]:
    #     ...

    # para sair
    if teclas[pygame.K_ESCAPE]:
        done = True

    t = clock.get_time()

    pygame.display.flip()

    clock.tick(fps)

pygame.quit()

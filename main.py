import os
import sys

from vector_2d import Vector
from typing import Optional

import pygame
from interactions import Interaction
from characters import Farmer, Character
from items import Tree, Mineral

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

farmer = Farmer(Vector(400, 400))
pressed_one: Optional[Character] = None
tree = Tree(Vector(200, 100))
mineral = Mineral(Vector(300, 50))

while not done:
    screen.fill(noir)
    tree.draw(screen)
    mineral.draw(screen)
    farmer.actualize(screen, t)
    for event in pygame.event.get():
        if event.type == pygame.MOUSEMOTION:
            if pressed_one:
                hovered = Interaction.get_hovered(Vector(*pygame.mouse.get_pos()), {tree, mineral})
                if hovered:
                    pygame.mouse.set_cursor(*pressed_one.get_cursor(hovered))
                else:
                    pygame.mouse.set_cursor(*pygame.cursors.arrow)
            else:
                pygame.mouse.set_cursor(*pygame.cursors.arrow)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                pressed_item = Interaction.get_hovered(Vector(*pygame.mouse.get_pos()), {tree, mineral})
                if pressed_item and pressed_one:
                    pressed_one.set_job(pressed_item)
                pressed_one = Interaction.mouse_characters(Vector(*pygame.mouse.get_pos()), {farmer, })
            if event.button == 3 and pressed_one:
                pressed_one.set_destination(Vector(*pygame.mouse.get_pos()))
            if event.button == 4:
                ...
            elif event.button == 5:
                ...
        if event.type == pygame.QUIT:
            done = True

    teclas = pygame.key.get_pressed()

    if teclas[pygame.K_KP_PLUS]:
        ...
    if teclas[pygame.K_KP_MINUS]:
        ...

    # para sair
    if teclas[pygame.K_ESCAPE]:
        done = True

    t = clock.get_time()
    fill = 0, 0, 0

    pygame.display.flip()

    clock.tick(fps)

pygame.quit()

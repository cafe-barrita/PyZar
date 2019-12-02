import os
import sys
from typing import Optional

import pygame
from vector_2d import Vector, VectorPolar

from characters import Character, Characters
from interactions import Interaction
from items import Mineral, Castle, Forest, Borders
from sea import Terrain

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
sea = Terrain(resolution)

while not done:
    screen.fill(noir)
    sea.draw(screen, t)
    mouse_vector = Vector(*pygame.mouse.get_pos())
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            done = True

    teclas = pygame.key.get_pressed()
    # para sair
    if teclas[pygame.K_ESCAPE]:
        done = True

    t = clock.get_time()

    pygame.display.flip()

    clock.tick(fps)

pygame.quit()

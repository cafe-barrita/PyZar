import os
import sys
from vector_2d import Vector

import pygame

from characters import Farmer

if sys.platform == 'win32' or sys.platform == 'win64':
    os.environ['SDL_VIDEO_CENTERED'] = '1'

pygame.init()
resolution = (800, 600)
pygame.display.set_caption('PyZar')
screen = pygame.display.set_mode(resolution)
clock = pygame.time.Clock()
t = clock.get_time()
done = False
fill = (0, 0, 0)
fps = 20

farmer = Farmer(Vector(400, 400))

while not done:
    screen.fill(fill)
    farmer.draw(screen)
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
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
    fill = (0, 0, 0)

    pygame.display.flip()

    clock.tick(fps)

pygame.quit()

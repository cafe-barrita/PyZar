import os
import sys

import pygame
from vector_2d import Vector

from terrain import Terrain

if sys.platform == 'win32' or sys.platform == 'win64':
    os.environ['SDL_VIDEO_CENTERED'] = '1'

pygame.init()
screen_resolution = 1000, 1000
side = 9e3
map_resolution = int(side), int(side)
pygame.display.set_caption('PyZar')
screen = pygame.display.set_mode(screen_resolution)
clock = pygame.time.Clock()
t = clock.get_time()
done = False
noir = 0, 0, 0
fps = 60
terrain = Terrain(screen_resolution, Vector(), map_resolution)
draw_contours = True

while not done:
    screen.fill(noir)
    terrain.draw(screen)
    mouse_vector = Vector(*pygame.mouse.get_pos())
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            done = True

    teclas = pygame.key.get_pressed()
    # para sair
    if teclas[pygame.K_t]:
        draw_contours = False
    else:
        draw_contours = True
    if teclas[pygame.K_ESCAPE]:
        done = True

    t = clock.get_time()

    pygame.display.flip()

    clock.tick(fps)

pygame.quit()

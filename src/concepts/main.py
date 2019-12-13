import asyncio
import collections
import os
import sys

import pygame
from pygame.rect import Rect
from vector_2d import Vector

from concepts.dijkstra import Path

if sys.platform == 'win32' or sys.platform == 'win64':
    os.environ['SDL_VIDEO_CENTERED'] = '1'

pygame.init()
screen_resolution = 1200, 800
pygame.display.set_caption('PyZar')
screen = pygame.display.set_mode(screen_resolution)
clock = pygame.time.Clock()
t = clock.get_time()
done = False
noir = 0, 0, 0
fps = 200
fps_to_show = collections.deque([fps] * fps)

font = pygame.font.Font('freesansbold.ttf', 20)
text = font.render('XX.X FPS', True, (255, 0, 0), (0, 0, 255))
text_rect: Rect = text.get_rect()
text_rect.bottomright = (screen_resolution[0] - 10, screen_resolution[1] - 20)
source = destination = None
path = Path(screen_resolution)
calculated = None

while not done:
    screen.fill(noir)
    mouse = Vector(*pygame.mouse.get_pos())
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                source = mouse
                destination = None
                calculated = False
            elif event.button == 3 and source:
                destination = mouse
                calculated = False

        elif event.type == pygame.QUIT:
            done = True
    if source:
        pygame.draw.circle(screen, (0, 0, 255), source.int(), 5)
        if destination:
            pygame.draw.circle(screen, (0, 255, 0), destination.int(), 5)
            if not calculated:
                # asyncio.run(path.get_dijkstra(source, destination))
                path.get_dijkstra(source, destination)
                calculated = True

    teclas = pygame.key.get_pressed()

    if teclas[pygame.K_ESCAPE]:
        done = True

    t = clock.get_time()
    if t != 0:
        fps_to_show.popleft()
        fps_to_show.append(1000 / t)
    text = font.render(f'{round(sum(fps_to_show) / len(fps_to_show), 1)} FPS', True, (255, 255, 0), (0, 0, 0))

    path.draw(screen)
    screen.blit(text, text_rect)
    pygame.display.flip()

    clock.tick(fps)

pygame.quit()

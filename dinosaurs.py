##BE CAREFUL IT MIGHT NOT CLOSE

import pygame
from pygame.locals import *

pygame.init()

# initial conditions

clock = pygame.time.Clock()

SCREEN = pygame.display.set_mode((500,500))


# Define some colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 170, 0)

done = False

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:   # If user clicked close
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:   # escape key is an escape
                done = True

    # workings

    # drawing
    SCREEN.fill(GREEN)

    pygame.display.flip()  # actually draws all that stuff.
    clock.tick(60)  # limits FPS

# if done becomes true:
pygame.quit

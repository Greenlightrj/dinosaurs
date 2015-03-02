import pygame
from pygame.locals import *

pygame.init()

    #initial contidions

clock = pygame.time.Clock()

done = False

while not done:

    SCREEN = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    scr_w, scr_h = SCREEN.get_size()

        #input
    for event in pygame.event.get():
        if event.type == pygame.QUIT: #if user presses the x button
            done = True
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.event.post(pygame.event.Event(QUIT)) #escape is an escape

    #workings

    #drawing
    screen.fill(BLACK)
    pygame.display.flip()   #actually draws all that stuff.
    clock.tick(60)  #limits FPS
#if done becomes true:
pygame.quit

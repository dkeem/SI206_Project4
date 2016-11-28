import random
import sys

import pygame
from pygame.locals import Rect, DOUBLEBUF, QUIT, K_ESCAPE, KEYDOWN, K_DOWN, \
    K_LEFT, K_UP, K_RIGHT, KEYUP, K_LCTRL, K_RETURN, FULLSCREEN

X_MAX = 800
Y_MAX = 600

LEFT, RIGHT, UP, DOWN = 0, 1, 3, 4
START, STOP = 0, 1


pygame.init()
screen = pygame.display.set_mode((X_MAX,Y_MAX))

gameExit = False
while not gameExit:
	for event in pygame.event.get():
		print(event)



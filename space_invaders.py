import pygame 
from pygame.locals import *

screen_width = 600
screen_height = 800

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Space Invaders")

run = True 
while run:
    for event in pygame.event.get():
        if event.type == QUIT:
            run = False

pygame.quit()
    


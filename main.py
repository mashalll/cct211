import pygame
from pygame.locals import *
pygame.init()
width = 900
height = 400
window = pygame.display.set_mode((width,height))
background = pygame.image.load('background.png')
background = pygame.transform.scale(background,(width,height))
 
 
runing = True
while runing:
    window.fill((0,0,0))
    window.blit(background,(0,-1))
    
    for event in pygame.event.get():
        if event.type == QUIT:
            runing = False
    pygame.display.update()
pygame.quit()

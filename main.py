import pygame
from pygame.locals import *

pygame.init()

#width and height for screen
width = 900
height = 400

#set up the background image
background = pygame.image.load('background.png')
background = pygame.transform.scale(background,(width,height))

class Sprite(pygame.sprite.Sprite):
    def __init__(self, image, startx, starty):
        super().__init__()
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.center = [startx, starty]
        
    def update(self):
        pass
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Platform(Sprite):
    def __init__(self, startx, starty):
        super().__init__("boxAlt.png",startx,starty)

def main():
    pygame.init()
    screen = pygame.display.set_mode((width,height))
    clock = pygame.time.Clock()


    #all sprites will be addede here 
    platforms = pygame.sprite.Group()
    
    #platform coordinates
    platforms.add(Platform(225, 365))



    #Exits game 
    done = True

    while done is True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = False
                
        pygame.event.pump()
    
        # Draw loop
        screen.fill((0,0,0))
        screen.blit(background,(0,-1))
        platforms.draw(screen)

        
        pygame.display.flip()
        platforms.update() 
        clock.tick(60)
    pygame.quit()


if __name__ == "__main__":
    main()

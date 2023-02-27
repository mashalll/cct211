import pygame
import spritesheet
from pygame.locals import *

pygame.init()

#width and height for screen
width = 900
height = 400

screen = pygame.display.set_mode((width, height))

# colour constants
BLACK = (0, 0, 0)

# loading sprite images
sprite_sheet_image = pygame.image.load('dino.png').convert_alpha()
sprite_sheet = spritesheet.SpriteSheet(sprite_sheet_image)
dinos = []
dinosteps = [4, 6, 3, 4]
action = 0
t = pygame.time.get_ticks()
cooldown = 100
frame = 0
count = 0

for x in dinosteps:
    temp = []
    for i in range(x):
        temp.append(sprite_sheet.get_image(count, 24, 24, 3, BLACK))
        count += 1
    dinos.append(temp)

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
        super().__init__("boxAlt.png", startx, starty)


def main():
    global t, frame, action
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
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and action > 0:
                    action -= 1
                    frame = 0
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT and action < len(dinos) - 1:
                    action += 1
                    frame = 0

        pygame.event.pump()

        # Draw loop
        screen.fill((0,0,0))
        screen.blit(background,(0,-1))
        platforms.draw(screen)

        # loading player images
        curr = pygame.time.get_ticks()
        if curr - t >= cooldown:
            frame += 1
            t = curr
            if frame >= len(dinos[action]):
                frame = 0

        screen.blit(dinos[action][frame], (0, 0))

        pygame.display.flip()
        platforms.update()
        clock.tick(60)
    pygame.quit()


if __name__ == "__main__":
    main()

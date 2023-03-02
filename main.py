import pygame
import numpy
import spritesheet
from pygame.locals import *

pygame.init()

#width and height for screen
width = 1500
height = 400

screen = pygame.display.set_mode((width, height))

# colour constants
BLACK = (0, 0, 0)

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


class Player(Sprite):
    change_y = 0

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # loading images
        sprite_sheet_image = pygame.image.load('dino.png').convert_alpha()
        sprite_sheet = spritesheet.SpriteSheet(sprite_sheet_image)

        self.dinos = []
        self.dinosteps = [4, 6, 3, 4]
        self.action = 0
        self.t = pygame.time.get_ticks()
        self.cooldown = 100
        self.frame = 1
        self.count = 0
        self.direction = True

        for x in self.dinosteps:
            temp = []
            for i in range(x):
                temp.append(sprite_sheet.get_image(self.count, 24, 24, 3, BLACK))
                self.count += 1
            self.dinos.append(temp)

        self.image = self.dinos[0][0]
        self.rect = self.image.get_rect()
        self.rect.y = 330

    def walk_animation(self):
        # updating walking frames
        curr = pygame.time.get_ticks()
        if curr - self.t >= self.cooldown:
            self.frame += 1
            self.t = curr
            if self.frame >= len(self.dinos):
                self.frame = 0

        # switching images based on direction
        if self.direction:
            self.image = self.dinos[self.action][self.frame]
        else:
            self.image = pygame.transform.flip(self.dinos[self.action][self.frame], True, False)

    def jump(self):
        self.change_y = -10

    def calc_grav(self):
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += .35

        # See if we are on the ground.
        if self.rect.y >= height - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = height - self.rect.height

    def check_collision(self, boxes):
        block_hit_list = pygame.sprite.spritecollide(self, boxes, False)
        for block in block_hit_list:
            if self.direction:
                self.rect.right = block.rect.left
            elif not self.direction:
                # Otherwise if we are moving left, do the opposite.
                self.rect.left = block.rect.right
                
    def check_under(self, boxes):
        block_hit_list = pygame.sprite.spritecollide(self, boxes, False)
        for block in block_hit_list:
            # Reset our position based on the top/bottom of the object.
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom
            self.change_y = 0
            
    def update(self, boxes):
        # moving the player in the direction they press
        self.calc_grav()
        if self.change_y > 0:
            self.check_under(boxes)

        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            self.rect.x -= 1
            self.action = 1
            self.direction = False
            self.walk_animation()
            self.check_collision(boxes)
        elif key[pygame.K_RIGHT]:
            self.rect.x += 1
            self.action = 1
            self.direction = True
            self.walk_animation()
            self.check_collision(boxes)
        else:
            self.action = 0
            self.walk_animation()

        self.rect.y += self.change_y

class Gem(Sprite):
    def __init__(self, startx, starty):
        super().__init__("gemBlue.png", startx, starty)
   

class Ledge (Sprite):
    def __init__(self, startx, starty):
        super().__init__("grassHalf.png", startx, starty)
        
class Lava (Sprite):
    def __init__(self, startx, starty):
        super().__init__("liquidLavaTop_mid.png", startx, starty)    


class Platform(Sprite):
    def __init__(self, startx, starty):
        super().__init__("boxAlt.png", startx, starty)


class MovablePlatform(Platform):
    def __init__(self, startx, starty, start, end, speed):
        super().__init__(startx, starty)
        self.start = start
        self.end = end
        self.speed = speed
        self.direction = numpy.sign(end - start)
    
    def update(self):
        self.rect.x += self.speed * self.direction
        if self.rect.x <= self.start:
            self.direction = numpy.sign(self.end - self.start)
        elif self.rect.x >= self.end:
            self.direction = numpy.sign(self.start - self.end)


def main():
    pygame.init()
    screen = pygame.display.set_mode((width,height))
    clock = pygame.time.Clock()


    #all sprites will be added here
    player = Player()

    players = pygame.sprite.Group()
    players.add(player)

    platforms = pygame.sprite.Group()
    dangerZone = pygame.sprite.Group()
    gems = pygame.sprite.Group()
    
    
    #platform coordinates
    platforms.add(Platform(225, 365))
    platforms.add(Platform(295, 365))
    platforms.add(Platform(365, 365))
    platforms.add(Platform(365, 295))
    platforms.add(Ledge(580, 170)) # PLACE COIN ABOVE THIS BLOCK
    platforms.add(Platform(755,295))
    
    platforms.add(Platform(755,365))
    
    platforms.add(MovablePlatform(485, 295, 400, 650, 1))
    
    #add danger zones
    dangerZone.add(Lava(435, 365))
    dangerZone.add(Lava(505, 365))
    dangerZone.add(Lava(575, 365))
    dangerZone.add(Lava(645, 365))
    dangerZone.add(Lava(715, 365))

    #add gem placement 
    gems.add(Gem(585, 115))
    


    #Exits game
    done = True

    while done is True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    player.jump()


        pygame.event.pump()

        # Draw loop
        screen.fill((0,0,0))
        screen.blit(background,(0,-1))
        dangerZone.draw(screen)
        platforms.draw(screen)
        gems.draw(screen)
        
        player.draw(screen)
        player.update(platforms)
        

        pygame.display.flip()
        platforms.update()
        dangerZone.update()
        gems.update()
        
        clock.tick(60)
    pygame.quit()


if __name__ == "__main__":
    main()

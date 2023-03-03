# Image Credits
# Bullet and Spaceship sprite: https://q.utoronto.ca/courses/288975/files/24417060?module_item_id=4444455
# Dinosaur sprite: https://arks.itch.io/dino-characters
# Block sprite: https://replit.com/talk/ask/Pygame-Sprite-Graphics/38044

# imports
import pygame
import numpy
import spritesheet
import random
from pygame.locals import *

pygame.init()

#width and height for screen
width = 1500
height = 400

screen = pygame.display.set_mode((width, height))
bullets = pygame.sprite.Group()

# colour constants
BLACK = (0, 0, 0)
clear = (0, 0, 0, 0)

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
        self.bg = True
        self.bullets = 0

        #set up the background image
        self.background = pygame.image.load('background.png')
        self.background = pygame.transform.scale(self.background,(width,height))

        # adding the frames of the player sprite to the dinos list 
        for x in self.dinosteps:
            temp = []
            for i in range(x):
                temp.append(sprite_sheet.get_image(self.count, 24, 24, 3, BLACK))
                self.count += 1
            self.dinos.append(temp)

        # setting the initial player display
        self.image = self.dinos[0][0]
        self.rect = self.image.get_rect()
        self.rect.y = 330

    def walk_animation(self):
        # updating the player's walking frames
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

    # citation: https://q.utoronto.ca/courses/288975/files/24582167?module_item_id=4467158
    def calc_grav(self):
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += .35

        # See if we are on the ground
        if self.rect.y >= height - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = height - self.rect.height

    def check_collision(self, boxes):
        block_hit_list = pygame.sprite.spritecollide(self, boxes, False)
        for block in block_hit_list:
            if self.direction:
                self.rect.right = block.rect.left
            elif not self.direction:
                # Otherwise if we are moving left, do the opposite
                self.rect.left = block.rect.right

    def check_under(self, boxes):
        block_hit_list = pygame.sprite.spritecollide(self, boxes, False)
        for block in block_hit_list:
            # Reset our position based on the top/bottom of the object
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom
            self.change_y = 0

    def update(self, boxes):
        self.calc_grav()
        if self.change_y > 0:
            self.check_under(boxes)

        # moving the player in the direction they press
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            self.rect.x -= 5
            self.action = 1
            self.direction = False
            self.walk_animation()
            self.check_collision(boxes)
        elif key[pygame.K_RIGHT]:
            self.rect.x += 5
            self.action = 1
            self.direction = True
            self.walk_animation()
            self.check_collision(boxes)
        else:
            self.action = 0
            self.walk_animation()

        self.rect.y += self.change_y

        # change background and increasing bullets once the player crosses the end
        if self.rect.x > 1400:
            if self.bg:
                self.bg = False
                self.background = pygame.image.load('background_01.png')
                self.background = pygame.transform.scale(self.background,(width,height))
                self.rect.x = 0
                self.bullets += 2
            else:
                self.bg = True
                self.background = pygame.image.load('background.png')
                self.background = pygame.transform.scale(self.background,(width,height))
                self.rect.x = 0
                self.bullets += 2


class Enemy(Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # loading images
        player_img = pygame.image.load("enemy.png").convert_alpha()
        self.image = pygame.transform.scale(player_img, (100, 100))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 20
        self.rect.x = 1400
        self.rect.y = 100
        self.speedy = 3

    def update(self, player):
        # moving the enemy from the bottom to the top of the screen
        self.rect.y += self.speedy
        if self.rect.y >= 350 or self.rect.y < 50:
            self.speedy = -self.speedy
        self.shoot(player)
        bullets.update()

    def shoot(self, player):
        # creating more bullets based on how many times the player crossed the screen
        while player.bullets >= len(bullets):
            b = Bullet(self.rect.x, random.randint(self.rect.top, self.rect.bottom))
            bullets.add(b)


class Bullet(Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        # loading images and setting start position
        self.image = pygame.image.load("laser.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x

    def update(self):
        # moving the bullet towards the player, killing it if it goes off screen
        self.rect.x -= 3
        if self.rect.x < 0:
            self.kill()

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

    enemies = pygame.sprite.Group()
    enemy = Enemy()
    enemies.add(enemy)

    platforms = pygame.sprite.Group()
    dangerZone = pygame.sprite.Group()
    gems = pygame.sprite.Group()


    #platform coordinates
    platforms.add(Platform(225, 365))
    platforms.add(Platform(295, 365))
    platforms.add(Platform(365, 365))
    platforms.add(Platform(365, 295))
    platforms.add(Ledge(580, 170))
    platforms.add(Platform(755,295))

    #Left wall border
    platforms.add(Platform(-50, 365))
    platforms.add(Platform(-50, 295))
    platforms.add(Platform(-50, 225))
    platforms.add(Platform(-50, 155))
    platforms.add(Platform(-50, 85))
    platforms.add(Platform(-50, 15))

    #Right wall border
    platforms.add(Platform(1535,0))
    platforms.add(Platform(1535,70))
    platforms.add(Platform(1535,140))
    platforms.add(Platform(1535,210))
    platforms.add(Platform(1535,280))
    platforms.add(Platform(1535,350))
    platforms.add(Platform(1535,420))


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
        screen.blit(player.background,(0,-1))

        for gem in gems:
            gem.draw(screen)

            for i in range(len(gems)):
                if player.rect.colliderect(gem.rect):
                    gem.image.fill(clear)

        for lava in dangerZone:
            dangerZone.draw(screen)

            for i in range(len(dangerZone)):
                if player.rect.colliderect(lava.rect):
                    done = False

        for enemy in enemies:
            enemy.draw(screen)
            for i in range(len(enemies)):
                if player.rect.colliderect(enemy.rect):
                    done = False

        for b in bullets:
            b.draw(screen)
            for i in range(len(bullets)):
                if player.rect.colliderect(b.rect):
                    done = False


        platforms.draw(screen)

        player.draw(screen)
        player.update(platforms)


        pygame.display.flip()
        platforms.update()
        dangerZone.update()
        gems.update()
        enemies.update(player)

        clock.tick(60)
    pygame.quit()


if __name__ == "__main__":
    main()


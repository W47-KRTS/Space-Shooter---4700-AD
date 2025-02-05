import pygame
from os.path import join   
import os
os.environ['SDL_AUDIODRIVER'] = 'dummy'
from random import randint, uniform  

import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

logger.debug("Program starting...")

# ramas la 2:39:00

class Player(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.image = pygame.image.load(join('images', 'player.png')).convert_alpha() #stores the surface
        self.rect = self.image.get_frect(midbottom = (window_width/2, window_height / 2))
        self.direction = pygame.Vector2()
        self.speed = 400

        #cooldown
        self.can_shoot = True
        self.laser_shoot_time = 0
        self.cooldown_duration = 200

    def laser_timer(self):
        if not self.can_shoot: #RUN code if the player cannot shoot
            current_time = pygame.time.get_ticks() # get the time continuesly
            if current_time - self.laser_shoot_time >= self.cooldown_duration: # runs continuously
                self.can_shoot = True


    def update(self, dt, *args, **kwargs):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
        self.direction = self.direction.normalize() if self.direction else self.direction
        self.rect.center += self.direction * self.speed * dt

        recent_keys = pygame.key.get_just_pressed()
        if recent_keys[pygame.K_SPACE] and self.can_shoot: # it s trigger only when the player shoots the laser
            Laser(laser_surf, self.rect.midtop, all_sprites)
            self.can_shoot = False
            self.laser_shoot_time = pygame.time.get_ticks()

        self.laser_timer()

class Star(pygame.sprite.Sprite):
    def __init__(self, *groups, surf):
        super().__init__(*groups)
        self.image = surf
        self.rect = self.image.get_frect(center = (randint(0, window_width), randint(0, window_height)))

class Laser(pygame.sprite.Sprite):
    def __init__(self, surf, pos, *groups):
        super().__init__(*groups)
        self.image = surf
        self.rect = self.image.get_frect(midbottom = pos)

    def update(self, dt):
        self.rect.centery -= 400 * dt
        if self.rect.bottom <= 0: # the laster left the window game
            self.kill() # destroy laser sprite

class Meteor(pygame.sprite.Sprite):
    def __init__(self, surf, pos, *groups):
        super().__init__(*groups)
        self.image = surf
        self.rect = self.image.get_frect(center = pos) # de modif
        self.start_time = pygame.time.get_ticks()
        self.lifetime = 3000
        self.direction = pygame.Vector2(uniform(-0.5,0.5), 1)
        self.speed = randint(350, 500)

    def update(self, dt):
        self.rect.center += self.direction * self.speed * dt
        if pygame.time.get_ticks() - self.start_time >= self.lifetime:
            self.kill()



# general setup

logger.debug("About to initialize pygame")
pygame.init()
logger.debug("Pygame initialized")


window_width, window_height = 1280, 720 
display_surface = pygame.display.set_mode((window_width, window_height))
running = True # variable to close the game
pygame.display.set_caption('Space Shooter - 4700 A.D.')
clock = pygame.time.Clock()

# imports
meteor_surf = pygame.image.load(join('images','meteor.png')).convert_alpha()
laser_surf = pygame.image.load(join('images','laser.png')).convert_alpha()
star_surf = pygame.image.load(join('images', 'star.png')).convert_alpha() #import the image once

logger.debug("imports")

# sprites
all_sprites = pygame.sprite.Group()

for i in range(20):
    Star(all_sprites, surf=star_surf) # using the same surface 20 times

player = Player(all_sprites) # create player after the stars

# custom events -> meteor event
meteor_event = pygame.event.custom_type()
pygame.time.set_timer(meteor_event, 400) # timer

while running:
    dt = clock.tick() / 1000
    
    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False # variable to close the game
        if event.type == meteor_event:
            x, y = randint(0, window_width), randint(-200, -100)
            Meteor(meteor_surf, (x,y), all_sprites)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                paused = not paused
     
    # update the game
    all_sprites.update(dt) # call an update method on the sprites in the group

    # Inside the game loop, after updating sprites
    meteor_collisions = pygame.sprite.spritecollide(player, all_sprites, dokill=True)
    if meteor_collisions:
        logger.debug("Player hit by meteor!")
        running = False  # End the game if the player is hit

    for laser in all_sprites:
        if isinstance(laser, Laser):
            meteor_hits = pygame.sprite.spritecollide(laser, all_sprites, dokill=True)
            for meteor in meteor_hits:
                if isinstance(meteor, Meteor):
                    logger.debug("Meteor destroyed!")

    # pause game
    if not paused:
        all_sprites.update(dt)
    else:
        font = pygame.font.Font(None, 74)
        text = font.render("Paused", True, 'white')
        display_surface.blit(text, (window_width // 2 - 100, window_height // 2 - 50))

    # draw the game
    display_surface.fill('skyblue3', rect=None, special_flags=0) # display the background color 
    all_sprites.draw(display_surface)

    # test collision
    player.rect.collidepoint((100,200))

    pygame.display.update() # update the entire window
   
pygame.quit() # the opposite of pygame.init()

import pygame
from os.path import join   

from random import randint  

# ramas la 2:08:00

class Player(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.image = pygame.image.load(join('images', 'player.png')).convert_alpha() #stores the surface
        self.rect = self.image.get_frect(midbottom = (window_width/2, window_height / 2))
        self.direction = pygame.Vector2()
        self.speed = 300

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
# general setup
pygame.init()

window_width, window_height = 1280, 720 
display_surface = pygame.display.set_mode((window_width, window_height))
running = True # variable to close the game
pygame.display.set_caption('Space Shooter - 4700 A.D.')
clock = pygame.time.Clock()

# plain surface
surf = pygame.Surface((100, 200))
surf.fill("orange")
x = 100


all_sprites = pygame.sprite.Group()

star_surf = pygame.image.load(join('images', 'star.png')).convert_alpha() #import the image once
for i in range(20):
    Star(all_sprites, surf=star_surf) # using the same surface 20 times

player = Player(all_sprites) # create player after the stars


# importing images
# player_surf = pygame.image.load(join('images','player.png')).convert_alpha()
# player_rect = player_surf.get_frect(midbottom = (window_width/2, window_height / 2))
# using frectangle to determine the position
# player_direction = pygame.math.Vector2() # (0,0)
# player_speed = 300



meteor_surf = pygame.image.load(join('images','meteor.png')).convert_alpha()
# meteor_rect = meteor_surf.get_frect(center = (window_width/2, window_height/2))

laser_surf = pygame.image.load(join('images','laser.png')).convert_alpha()
# laser_rect = laser_surf.get_frect(bottomleft = (20, window_height - 50))

# star_surf =  pygame.image.load(join('images','star.png')).convert_alpha()
# star_position = [(randint(0,window_width), randint(0, window_height)) for i in range (50)]
# drawing stars in random positions

# custom events -> meteor event
meteor_event = pygame.event.custom_type()
pygame.time.set_timer(meteor_event, 500) # timer


while running:
    dt = clock.tick() / 1000
    
    # event loop

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False # variable to close the game
        if event.type == meteor_event:
            print("create meteor")
        #if event.type == pygame.KEYDOWN and event.key == pygame.K_1:
        #    print(1)
        #if event.type == pygame.MOUSEMOTION:
        #    player_rect.center = event.pos

    # input
    # keys = pygame.key.get_pressed()
    # player_direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])  # player to right when right key is pressed
    # player_direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
    # player_direction = player_direction.normalize() if player_direction else player_direction 
    # make the diagonal movement 1 by making x and y smaller
    # player_rect.center += player_direction * player_speed * dt

    # recent_keys = pygame.key.get_just_pressed()
    # if recent_keys[pygame.K_SPACE]:
    #    print('fire laser')

    # update the game

    all_sprites.update(dt) # call an update method on the sprites in the group

    # draw the game
    display_surface.fill('skyblue3', rect=None, special_flags=0) # display the background color 
    
    # for position in star_position: # display the stars
    #    display_surface.blit(star_surf, position)
        
    # display_surface.blit(meteor_surf, meteor_rect) # display meteor
    # display_surface.blit(laser_surf, laser_rect) # display laser
    # display_surface.blit(player_surf, player_rect) # display the player ship

    all_sprites.draw(display_surface)


    pygame.display.update() # update the entire window

    

pygame.quit() # the opposite of pygame.init()

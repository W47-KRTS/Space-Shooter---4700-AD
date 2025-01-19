import pygame
from os.path import join   
from random import randint  
# ramas la 54:27

# general setup

pygame.init()

window_width, window_height = 1280, 720 
display_surface = pygame.display.set_mode((window_width, window_height))
running = True # variable to close the game
pygame.display.set_caption('The Space Shooter - 4700 A.D.')

# plain surface
surf = pygame.Surface((100, 200))
surf.fill("orange")
x = 100

# importing images
player_surf = pygame.image.load(join('images','player.png')).convert_alpha()
player_rect = player_surf.get_frect(midbottom = (window_width/2, window_height-20))
player_direction = 1
# using frectangle to determine the position

meteor_surf = pygame.image.load(join('images','meteor.png')).convert_alpha()
meteor_rect = meteor_surf.get_frect(center = (window_width/2, window_height/2))

laser_surf = pygame.image.load(join('images','laser.png')).convert_alpha()
laser_rect = laser_surf.get_frect(center = (window_width/2, window_height/-50))

star_surf =  pygame.image.load(join('images','star.png')).convert_alpha()
star_position = [(randint(0,window_width), randint(0, window_height)) for i in range (50)]
# drawing stars in random positions

while running:
    # event loop

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False # variable to close the game


    # draw the game
    display_surface.fill('skyblue3', rect=None, special_flags=0) # display the background color 
    for position in star_position: # display the stars
        display_surface.blit(star_surf, position)
        
    display_surface.blit(meteor_surf, meteor_rect) # display meteor
    display_surface.blit(laser_surf, meteor_rect) # display meteor

    pygame.display.update() # update the entire window
    

    # player movement
    player_rect.x += player_direction * 0.4
    if player_rect.right > window_width or player_rect.left < 0: # keeping the player ship onto screen
        player_direction *= -1 
    display_surface.blit(player_surf, player_rect) # display the player ship


pygame.quit() # the opposite of pygame.init()

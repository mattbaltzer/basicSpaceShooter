import pygame
from os.path import join
from random import randint

# pygame setup
pygame.init()
window_width, window_height = 1280, 720
display_surface = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('Space shooter')
clock = pygame.time.Clock()
running = True

# importing an image -> image becomes an surface when it is imported
# imports :
player_surf = pygame.image.load(join('images', 'player.png')).convert_alpha()
player_rect = player_surf.get_frect(center = (window_width / 2, window_height /2 + 100))
player_direction = pygame.math.Vector2()
player_speed = 300

star_surf = pygame.image.load(join('images', 'star.png')).convert_alpha()
star_positions = [(randint(0, window_width), randint(0, window_height)) for i in range(20)]

meteor_surf = pygame.image.load(join('images', 'meteor.png')).convert_alpha()
meteor_rect = meteor_surf.get_frect(center = (window_width / 2, window_height / 2))

laser_surf = pygame.image.load(join('images', 'laser.png')).convert_alpha()
laser_rect = laser_surf.get_frect(bottomleft = (20, window_height - 20))


while running:
    dt = clock.tick() / 1000
    # event loop
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if event.type == pygame.KEYDOWN and event.key == pygame.K_1:
        #     print(1)
        # if event.type == pygame.MOUSEMOTION:
        #     player_rect.center = event.pos 

    # inputs
    # print(pygame.mouse.get_rel())
    keys = pygame.key.get_pressed()
    player_direction.y = int(keys[pygame.K_s]) - int(keys[pygame.K_w])
    player_direction.x = int(keys[pygame.K_d]) - int(keys[pygame.K_a])
    

    player_rect.center += player_direction * player_speed * dt

    # fill the screen with a color to wipe away anything from last frame
    display_surface.fill('black')
    for pos in star_positions:
        display_surface.blit(star_surf, pos)
    

    # if player_rect.right >= window_width or player_rect.left <= 0:
    #     player_direction.x *= -1
    # if player_rect.top <= 0 or player_rect.bottom >= window_height:
    #     player_direction.y *= -1

    display_surface.blit(meteor_surf, meteor_rect)
    display_surface.blit(laser_surf, laser_rect)

    # player movement
    # This is the standard for moving something in pygame. rect.center += direction * speed * delta time
    
    display_surface.blit(player_surf,player_rect)
    

    # flip the display to put your work on the screen
    pygame.display.update() # can also use pygame.display.flip() -> can update specific parts instead of the whole thing

pygame.quit()
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

# basic surface
surf = pygame.Surface((100,200))
surf.fill('orange')
x = 100

# importing an image -> image becomes an surface when it is imported
player_surf = pygame.image.load(join('images', 'player.png')).convert_alpha()
player_rect = player_surf.get_frect(center = (window_width / 2, window_height /2))

star_surf = pygame.image.load(join('images', 'star.png')).convert_alpha()
star_positions = [(randint(0, window_width), randint(0, window_height)) for i in range(20)]

while running:
    # event loop
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    display_surface.fill('black')
    for pos in star_positions:
        display_surface.blit(star_surf, pos)
    if player_rect.right < window_width:
        player_rect.left += 3
    display_surface.blit(player_surf,player_rect)

    # flip the display to put your work on the screen
    pygame.display.update() # can also use pygame.display.flip() -> can update specific parts instead of the whole thing

    # limits the FPS to 60
    clock.tick(60)  


pygame.quit()
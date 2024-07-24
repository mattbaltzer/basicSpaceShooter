import pygame
from os.path import join
from random import randint

class Player(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.image = pygame.image.load(join('images', 'player.png')).convert_alpha()
        self.rect = self.image.get_frect(center = (window_width / 2, window_height /2 + 100))
        self.direction = pygame.math.Vector2()
        self.speed = 300

        # timer(cooldown)
        self.can_shoot = True
        self.laser_shoot_time = 0
        self.cooldown_duration = 500

    def laser_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_shoot_time >= self.cooldown_duration:
                self.can_shoot = True

    def inputs(self):
        # print(pygame.mouse.get_rel())
        keys = pygame.key.get_pressed()
        self.direction.y = int(keys[pygame.K_s]) - int(keys[pygame.K_w])
        self.direction.x = int(keys[pygame.K_d]) - int(keys[pygame.K_a])
        self.direction = self.direction.normalize() if self.direction else self.direction
        self.rect.center += self.direction * self.speed * dt # This is the standard for moving something in pygame. rect.center += direction * speed * delta time

        recent_keys = pygame.key.get_just_pressed()
        if recent_keys[pygame.K_SPACE] and self.can_shoot:
            print('fire laser')
            self.can_shoot = False
            self.laser_shoot_time = pygame.time.get_ticks()

        self.laser_timer()

        # if player_rect.right >= window_width or player_rect.left <= 0:
        #     player_direction.x *= -1
        # if player_rect.top <= 0 or player_rect.bottom >= window_height:
        #     player_direction.y *= -1

    def update(self, dt):
        self.inputs()
        
class Star(pygame.sprite.Sprite):
    def __init__(self, groups, surf):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center = (randint(0, window_width), randint(0, window_height)))

# pygame setup
pygame.init()
window_width, window_height = 1280, 720
display_surface = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('Space shooter')
clock = pygame.time.Clock()
running = True

# groups
all_sprites = pygame.sprite.Group()
star_surf = pygame.image.load(join('images', 'star.png')).convert_alpha()
for i in range(20):
    Star(all_sprites, star_surf)
player = Player(all_sprites)

meteor_surf = pygame.image.load(join('images', 'meteor.png')).convert_alpha()
meteor_rect = meteor_surf.get_frect(center = (window_width / 2, window_height / 2))

laser_surf = pygame.image.load(join('images', 'laser.png')).convert_alpha()
laser_rect = laser_surf.get_frect(bottomleft = (20, window_height - 20))

# custom events -> meteor event, customer timer that creates sprites
meteor_event = pygame.event.custom_type()
pygame.time.set_timer(meteor_event, 2000)


while running:
    dt = clock.tick() / 1000
    # event loop
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == meteor_event:
            print('create meteor')
    # updating the game
    all_sprites.update(dt)

    # draw the game
    display_surface.fill('black')
    all_sprites.draw(display_surface)    
    pygame.display.update()

pygame.quit()
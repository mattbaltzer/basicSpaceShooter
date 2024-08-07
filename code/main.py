import pygame
from os.path import join
from random import randint, uniform

class Player(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.image =  pygame.image.load(join('images', 'player.png')).convert_alpha()
        self.rect = self.image.get_frect(center = (window_width / 2, window_height /2 + 100))
        self.direction = pygame.math.Vector2()
        self.speed = 300

        # timer(cooldown)
        self.can_shoot = True
        self.laser_shoot_time = 0
        self.cooldown_duration = 500

        # mask
        self.mask = pygame.mask.from_surface(self.image)
        
    def laser_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_shoot_time >= self.cooldown_duration:
                self.can_shoot = True
                

    def update(self, dt):
        # print(pygame.mouse.get_rel())
        keys = pygame.key.get_pressed()
        self.direction.y = int(keys[pygame.K_s]) - int(keys[pygame.K_w])
        self.direction.x = int(keys[pygame.K_d]) - int(keys[pygame.K_a])
        self.direction = self.direction.normalize() if self.direction else self.direction
        self.rect.center += self.direction * self.speed * dt # This is the standard for moving something in pygame. rect.center += direction * speed * delta time

        recent_keys = pygame.key.get_just_pressed()
        if recent_keys[pygame.K_SPACE] and self.can_shoot:
            Laser(laser_surf, self.rect.midtop, (all_sprites, laser_sprites))
            self.can_shoot = False
            self.laser_shoot_time = pygame.time.get_ticks()
            laser_sound.play()
            laser_sound.set_volume(0.05)

        self.laser_timer()

        # if player_rect.right >= window_width or player_rect.left <= 0:
        #     player_direction.x *= -1
        # if player_rect.top <= 0 or player_rect.bottom >= window_height:
        #     player_direction.y *= -1

class Star(pygame.sprite.Sprite):
    def __init__(self, groups, surf):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center = (randint(0, window_width), randint(0, window_height)))

class Laser(pygame.sprite.Sprite):
    def __init__(self, surf, pos, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(midbottom = pos)

    def update(self, dt):
        self.rect.centery -= 400 * dt
        if self.rect.bottom < 0:
            self.kill()

class Meteor(pygame.sprite.Sprite):
    def __init__(self, surf, pos, groups):
        super().__init__(groups)
        self.original_surf = surf
        self.image = self.original_surf
        self.rect = self.image.get_frect(center = pos)
        self.start_time = pygame.time.get_ticks()
        self.lifetime = 3000
        self.direction = pygame.Vector2(uniform(-0.5, 0.5),1)
        self.speed = randint(400, 500)
        self.rotation_speed = randint(40, 120)
        self.rotation = 0

    def update(self, dt):
        self.rect.center += self.direction * self.speed * dt
        if pygame.time.get_ticks() - self.start_time >= self.lifetime:
            self.kill()

        # continuous rotation
        self.rotation += self.rotation_speed * dt
        self.image = pygame.transform.rotozoom(self.original_surf, self.rotation, 1)
        self.rect = self.image.get_frect(center = self.rect.center)

class Explosion(pygame.sprite.Sprite):
    def __init__(self, frames, pos, groups):
        super().__init__(groups)
        self.frames = frames
        self.frame_index = 0
        self.image = frames[self.frame_index]
        self.rect = self.image.get_frect(center = pos)

    def update(self, dt):
        self.frame_index += 20 * dt
        if self.frame_index < len(self.frames):
            self.image = self.frames[int(self.frame_index)]
        else:
            self.kill()

def collisions():
    global running
    if pygame.sprite.spritecollide(player, meteor_sprites, True, pygame.sprite.collide_mask):
        running = False

    for laser in laser_sprites:
        if pygame.sprite.spritecollide(laser, meteor_sprites, True):
            laser.kill()
            Explosion(explosion_frames, laser.rect.midtop, all_sprites)
            explosion_sound.play()
            explosion_sound.set_volume(0.1)

def display_score():
    current_time = pygame.time.get_ticks() // 10
    text_surf = font.render(str(current_time), True, '#fffef4')
    text_rect = text_surf.get_frect(midbottom = (window_width / 2 , window_height - 50))
    display_surface.blit(text_surf, text_rect)
    pygame.draw.rect(display_surface, '#fffef4', text_rect.inflate(20,10).move(0, -7), 5, 10)

# pygame setup
pygame.init()
window_width, window_height = 1280, 720
display_surface = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('Space shooter')
clock = pygame.time.Clock()
running = True

# imports
font = pygame.font.Font(join('images', 'Oxanium-Bold.ttf'), 50)
star_surf = pygame.image.load(join('images', 'star.png')).convert_alpha()
meteor_surf = pygame.image.load(join('images', 'meteor.png')).convert_alpha()
laser_surf = pygame.image.load(join('images', 'laser.png')).convert_alpha()
explosion_frames = [pygame.image.load(join('images', 'explosion', f'{i}.png')).convert_alpha() for i in range(21)]

laser_sound = pygame.mixer.Sound(join('audio', 'laser.wav'))
explosion_sound = pygame.mixer.Sound(join('audio', 'explosion.wav'))
game_music = pygame.mixer.Sound(join('audio', 'game_music.wav'))
game_music.set_volume(0.05)
game_music.play(loops = -1)

# groups
all_sprites = pygame.sprite.Group()
meteor_sprites = pygame.sprite.Group()
laser_sprites = pygame.sprite.Group()
explosion_sprites = pygame.sprite.Group()
for i in range(20):
    Star(all_sprites, star_surf)
player = Player(all_sprites)

# custom events -> meteor event, customer timer that creates sprites
meteor_event = pygame.event.custom_type()
pygame.time.set_timer(meteor_event, 200)


while running:
    dt = clock.tick() / 1000
    # event loop
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == meteor_event:
            x, y = randint(0, window_width), randint(-200, -100)
            Meteor(meteor_surf, (x,y), (all_sprites, meteor_sprites))
    # updating the game
    all_sprites.update(dt)
    collisions()
    

    # draw the game
    display_surface.fill('#3a2e3f')
    display_score()
    all_sprites.draw(display_surface)

    pygame.display.update()

pygame.quit()
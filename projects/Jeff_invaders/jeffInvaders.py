''' JEFF INVADERS
program by: J. Butcher
art by: Jeff

explosion animation from:  https://www.kenney.nl/assets
logo font: Xirod by Raymond Larabie
other font: Vezla by Jorge Algarin
'''
import math
import random
from os import path

import pygame
from pygame.locals import *

img_dir = path.join(path.dirname(__file__), 'img')
snd_dir = path.join(path.dirname(__file__), 'snd')
WIDTH = 1366
HEIGHT = 710
FPS = 60

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
JEEP = (0, 115, 230)

# initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("JEFF Invaders 2")
clock = pygame.time.Clock()

font_name = pygame.font.match_font('arial')
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font('vezla.ttf', 30)
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

def draw_logo(surf, text, size, x, y):
    font = pygame.font.Font('xirod.ttf', 80)
    text_surface = font.render(text, True, JEEP)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

def draw_sheild_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = BAR_LENGTH * pct // 100  #remember# to ge the percent of a variable#
    outline_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)

def newmob():
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (100, 100))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 65
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.sheild = 800
        self.shoot_delay = 200
        self.last_shot = pygame.time.get_ticks()
        pos = pygame.mouse.get_pos()

    def update(self):
        # Get the current mouse position. This returns the position
        # as a list of two numbers.
        pos = pygame.mouse.get_pos()

        # Fetch the x and y out of the list
        # NOTE: If you want to keep the mouse at the bottom of the screen, just
        # set y = 380, and not update it with the mouse position stored in
        # pos[1]
        x = pos[0]
        y = 600  ## locks player to botom or top##

        # Set the attribute for the top left corner where this object is
        # located
        self.rect.x = x
        self.rect.y = y

        keystate = pygame.key.get_pressed()
        self.shoot()
        self.rect.x += self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.shoot()
            if event.type == pygame.MOUSEMOTION:
                self.shoot()
            #pygame.key.set_repeat(30, 500)
           # if event.type == pygame.MOUSEMOTION: 1

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            bullet = Bullet(self.rect.centerx, self.rect.top)
            all_sprites.add(bullet)
            bullets.add(bullet)
            #shoot_sound.play()

class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = random.choice(meteor_images)
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .85 / 2)
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-150, -100)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-3, 3)
        self.rot = 0
        self.rot_speed = random.randrange(-8, 8)
        self.last_update = pygame.time.get_ticks()

    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self):
        self.rotate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(8, 20)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.image = pygame.transform.scale(bullet_img, (25, 75))
        self.image_orig = random.choice(flop_list)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .85 / 2)
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(8, 20)
        # kill if it moves off the top of the screen
        if self.rect.bottom < 0:
            self.kill()
           # expl = Explosion(hit.rect.center, 'pf')


# show splash screen
def show_go_screen():
    screen.blit(background, background_rect)
    draw_logo(screen, "Jeff Invaders", 90, WIDTH / 2, HEIGHT / 4)
    #draw_text(screen, "Mouse Moves the Boat", 35, WIDTH / 2, HEIGHT / 2)
    #draw_text(screen, "Click Anywhere to Start", 35, WIDTH / 2, HEIGHT * 3 / 4)
    with open ('scores.txt', 'r') as f:
        highscore = int(f.read())
        draw_text(screen, ("HIGH SCORE"), 28, WIDTH / 2, 15)
        draw_text(screen, str(highscore), 28, WIDTH / 2, 45)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                waiting = False

# show high score screen
def score_screen():
    screen.blit(background, background_rect)
    draw_logo(screen, "New High Score!", 90, WIDTH / 2, HEIGHT / 4)
    #draw_text(screen, "Mouse Moves the Boat", 35, WIDTH / 2, HEIGHT / 2)
    #draw_text(screen, "Click Anywhere to Start", 35, WIDTH / 2, HEIGHT * 3 / 4)
    with open ('scores.txt', 'r') as f:
        highscore = int(f.read())
        draw_text(screen, ("HIGH SCORE"), 28, WIDTH / 2, 15)
        draw_text(screen, str(highscore), 28, WIDTH / 2, 45)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                waiting = False


# Load all game graphics
background = pygame.image.load(path.join(img_dir, "back.png")).convert()
background_rect = background.get_rect()
player_img = pygame.image.load(path.join(img_dir, "boat.png")).convert()
bullet_img = pygame.image.load(path.join(img_dir, "flip1.png")).convert()
hit_exp = pygame.image.load(path.join(img_dir, "exp.png")).convert()

exp_2 = []
flop_list = []
meteor_images = []
meteor_list = ['jeffy1.png', 'jeffy2.png', 'jeffy3.png']
flop_list = ['flip1.png, flip2.png, flip3.png, flip4.png']
for img in meteor_list:
    meteor_images.append(pygame.image.load(path.join(img_dir, img)).convert())

explosion_anim = {}
explosion_anim['lg'] = []
explosion_anim['sm'] = []
explosion_anim['pf'] = []
for i in range(9):
    filename = 'expl1{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(BLACK)
    img_lg = pygame.transform.scale(img, (100, 100))
    explosion_anim['lg'].append(img_lg)
    img_sm = pygame.transform.scale(img, (100, 100))
    filename = 'puff1{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(BLACK)
    explosion_anim['sm'].append(img_sm)
    img_pf = pygame.transform.scale(img, (185, 185))
    explosion_anim['pf'].append(img_pf)

# load all game sounds
shoot_sound = pygame.mixer.Sound(path.join(snd_dir, 'sfx_zap.ogg'))
expl_sound = pygame.mixer.Sound(path.join(snd_dir, 'sfx_shieldDown.ogg'))
hit_sound = pygame.mixer.Sound(path.join(snd_dir, 'sfx_twoTone.ogg'))

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 2
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 10

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

def __init__(self, x, y):
    pygame.sprite.Sprite.__init__(self)
    self.image = bullet_img
    self.image.set_colorkey(BLACK)
    self.rect = self.image.get_rect()
    self.rect.bottom = y
    self.rect.centerx = x
    self.speedy = -10

# Game loop
game_over = True
running = True
while running:
    if game_over:
        show_go_screen()
        game_over = False
        all_sprites = pygame.sprite.Group()
        mobs = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)
        for i in range(8):
            newmob()
        score = 0

    # keep loop running at the right speed
    clock.tick(FPS)

    # Process input (events)

    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            pygame.quit()

    # Update
    all_sprites.update()

    # check to see if a bullet hit a mob
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for hit in hits:
        score += 50
        hit_sound.play()
        expl = Explosion(hit.rect.center, 'lg')
        all_sprites.add(expl)
        newmob()

    # check to see if a mob hit the player
    hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)
    for hit in hits:
        newmob()
        newmob()
        newmob()
        player.sheild -= hit.radius * 2
        expl_sound.play()
        expl = Explosion(hit.rect.center, 'pf')
        all_sprites.add(expl)
        if player.sheild <= 0:
            score -= 1
            game_over = True
            with open ('scores.txt', 'r') as f:
                try:
                    highscore = int(f.read())
                except:
                    highscore = 0
            if score > highscore:
                score_screen()
                #print("New High Score")
                #print(str(score))
                with open ('scores.txt', 'w') as f:
                    highscore = int(f.write(str(score)))


    # Draw / render
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)

    # Draw score / highscore
    draw_text(screen,("Score"), 28, WIDTH / 8, 15)
    draw_text(screen, str(score), 28, WIDTH / 8, 45)
    with open ('scores.txt', 'r') as f:
        highscore = int(f.read())
        draw_text(screen, ("HIGH SCORE"), 28, WIDTH / 2, 15)
        draw_text(screen, str(highscore), 28, WIDTH / 2, 45)
    draw_sheild_bar(screen, 5, 5, player.sheild)

    # *after* drawing everyt hing, flip the display
    pygame.display.flip()

pygame.quit()


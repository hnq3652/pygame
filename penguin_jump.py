import pygame as pg
from pygame.locals import*
import random

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_SPEED = 10
ENEMY_SPEED = 25
JUMP_POWER = -65
GRAVITY = 5
FPS = 30

def __init__():
    pg.init()
    load_data()
    reset()
    while True:
        update()
        draw()
        pg.display.update()
        for event in pg.event.get():
            if event.type == QUIT or pg.key.get_pressed()[K_ESCAPE]:
                return
        pg.time.Clock().tick(FPS)

def load_data():
    global screen, player_image, enemy_image, fish_image, font
    screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    player_image_1 = pg.transform.smoothscale(pg.image.load("images/penguin_left.png").convert_alpha(), (80, 80))
    player_image_2 = pg.transform.smoothscale(pg.image.load("images/penguin_right.png").convert_alpha(), (80, 80))
    player_image_3 = pg.transform.smoothscale(pg.image.load("images/penguin_death.png").convert_alpha(), (80, 80))
    player_image = [player_image_1, player_image_2, player_image_3]
    enemy_image = pg.transform.smoothscale(pg.image.load("images/icicle.png").convert_alpha(), (80, 80))
    fish_image = pg.transform.smoothscale(pg.image.load("images/fish.png").convert_alpha(), (80, 80))
    font = pg.font.SysFont('meiryo', 55)

def reset():
    global player, player_dir, is_jumping, jump_speed, enemies, enemies_wait_time, player_alive, fish, score
    player = player_image[0].get_rect(x=350, y=520)
    player_dir = 'left'
    is_jumping = False
    jump_speed = 0
    enemies = [enemy_image.get_rect(x=100*i, y=0) for i in range(8)]
    enemies_wait_time = [random.randint(30,210) for i in range(8)]
    player_alive = True
    fish = fish_image.get_rect(x=350, y=400)
    score = 0

def update():
    if player_alive:
        update_player_x()
        update_player_y()
        update_enemies()
        check_collision()
        check_fish_get()
    else:
        if pg.key.get_pressed()[K_r]:
            reset()

def update_player_x():
    global player, player_dir
    if pg.key.get_pressed()[K_a]:
        player.x = player.x - PLAYER_SPEED
        player_dir = 'left'
    elif pg.key.get_pressed()[K_d]:
        player.x = player.x + PLAYER_SPEED
        player_dir = 'right'
    player.clamp_ip((0, 0), (SCREEN_WIDTH, SCREEN_HEIGHT))

def update_player_y():
    global player, is_jumping, jump_speed
    if is_jumping:
        jump_speed = jump_speed + GRAVITY
        player.y = player.y + jump_speed
        if player.y > 520:
            player.y = 520
            is_jumping = False
    elif pg.key.get_pressed()[K_SPACE] and not is_jumping:
        is_jumping = True
        jump_speed = JUMP_POWER

def update_enemies():
    global enemies, enemies_wait_time
    for i in range(len(enemies)):
        enemies_wait_time[i] = enemies_wait_time[i] - 1
        if enemies[i].y < 0:
            enemies[i].y = enemies[i].y + 5
        if enemies_wait_time[i] <= 0:
            enemies[i].y = enemies[i].y + ENEMY_SPEED
            if enemies[i].y > SCREEN_HEIGHT+60:
                enemies[i].y = -80
                enemies_wait_time[i] = random.randint(30,210)
        elif enemies_wait_time[i] <= 18:  #つらら震えるやつ
            if enemies_wait_time[i]%6 == 0:
                enemies[i].x = enemies[i].x + 10
            elif enemies_wait_time[i]%3 == 0:
                enemies[i].x = enemies[i].x - 10

def check_collision():
    global player_alive
    for i in range(len(enemies)):
        if player.colliderect(enemies[i]):
            player_alive = False

def check_fish_get():
    global fish, score
    if player.colliderect(fish):
        score = score + 1
        fish.x = random.randint(0, SCREEN_WIDTH-80)
        fish.y = random.randint(80, SCREEN_HEIGHT-80)

def draw():
    screen.fill((169, 193, 255))
    if not player_alive:
        screen.blit(player_image[2], player)
    elif player_dir == 'left':
        screen.blit(player_image[0], player)
    else:
        screen.blit(player_image[1], player)
    for i in range(len(enemies)):
        screen.blit(enemy_image, enemies[i])
    screen.blit(fish_image, fish)
    str_score = font.render(f'{score}', True, (0, 0, 0))
    screen.blit(str_score, (0,0))
    if not player_alive:
        message = font.render('press R to continue', True, (0, 0, 0))
        screen.blit(message, (150,280))

__init__()
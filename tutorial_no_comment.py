import pygame as pg
from pygame.locals import*

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_SPEED = 5
FPS = 30

def __init__():
    global screen, player_image, player
    pg.init()
    screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    player_image = pg.transform.smoothscale(pg.image.load("images/robonyan.png").convert_alpha(), (60, 60))
    player = player_image.get_rect(x=0, y=200)
    while True:
        update()
        draw()
        pg.display.update()
        for event in pg.event.get():
            if event.type == QUIT or pg.key.get_pressed()[K_ESCAPE]:
                return
        pg.time.Clock().tick(FPS)

def update():
    global player
    if pg.key.get_pressed()[K_w]:
        player.y = player.y - PLAYER_SPEED
    elif pg.key.get_pressed()[K_s]:
        player.y = player.y + PLAYER_SPEED
    if pg.key.get_pressed()[K_a]:
        player.x = player.x - PLAYER_SPEED
    elif pg.key.get_pressed()[K_d]:
        player.x = player.x + PLAYER_SPEED
    player.clamp_ip((0, 0), (SCREEN_WIDTH, SCREEN_HEIGHT))

def draw():
    screen.fill((0, 0, 0))
    screen.blit(player_image, player)

__init__()
import pygame as pg
from pygame.locals import*

def __init__():
    global screen, player_color, player
    pg.init()
    screen = pg.display.set_mode((800, 600))
    player_color = (0, 255, 255)
    player = Rect((0, 200), (60, 60))
    while True:
        update()
        draw()
        pg.display.update()
        for event in pg.event.get():
            if event.type == QUIT or pg.key.get_pressed()[K_ESCAPE]:
                return
        pg.time.Clock().tick(30)

def update():
    global player
    player.x = player.x + 5
    if player.x > 800:
        player.x = 0

def draw():
    screen.fill((0, 0, 0))
    pg.draw.rect(screen, player_color, player)

__init__()
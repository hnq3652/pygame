import pygame as pg
from pygame.locals import*
import random

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_SPEED = 5
FPS = 30

def __init__():
    global screen, player_image, player, character
    pg.init()
    screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    player_image_1 = pg.transform.smoothscale(pg.image.load("images/robonyan.png").convert_alpha(), (60, 60))
    player_image_2 = pg.transform.smoothscale(pg.image.load("images/nezubotto.png").convert_alpha(), (60, 60))
    player_image = [player_image_1, player_image_2]  #各画像を要素とした配列を用意
    player = player_image[random.randint(0,1)].get_rect(x=0, y=200)  #画像と長方形を対応させる(1種類だけすればokらしい)
    character = 0
    while True:
        update()
        draw()
        pg.display.update()
        for event in pg.event.get():  #イベント処理は一か所でまとめた方がよさそう(分けて毎回ループ回すと重たい?)
            if event.type == QUIT or pg.key.get_pressed()[K_ESCAPE]:
                return
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:    #スペースキーがそのフレームに押されたら(長押し不可)
                character ^= 1
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
    screen.blit(player_image[character], player)  #player_imageの番号指定して絵柄切り替える

__init__()
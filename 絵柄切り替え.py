import pygame as pg
from pygame.locals import*
import random

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_SPEED = 5
FPS = 30

def __init__():
    global screen, player_image, player, character, events
    pg.init()
    screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    player_image_1 = pg.transform.smoothscale(pg.image.load("images/robonyan.png").convert_alpha(), (60, 60))
    player_image_2 = pg.transform.smoothscale(pg.image.load("images/nezubotto.png").convert_alpha(), (60, 60))
    player_image = [player_image_1, player_image_2]  #各画像を要素とした配列を用意
    player = player_image[random.randint(0,1)].get_rect(x=0, y=200)  #画像と長方形を対応させる(1種類だけすればokらしい)
    character = 0
    while True:
        events = []  #そのフレーム間に起こったイベントを保存する配列を用意
        for event in pg.event.get():  #eventsに全てのイベントを追加
            events.append(event)
        update()
        draw()
        pg.display.update()
        for event in events:
            if event.type == QUIT or pg.key.get_pressed()[K_ESCAPE]:
                return
        pg.time.Clock().tick(FPS)

def update():
    global player, character
    if pg.key.get_pressed()[K_w]:
        player.y = player.y - PLAYER_SPEED
    elif pg.key.get_pressed()[K_s]:
        player.y = player.y + PLAYER_SPEED
    if pg.key.get_pressed()[K_a]:
        player.x = player.x - PLAYER_SPEED
    elif pg.key.get_pressed()[K_d]:
        player.x = player.x + PLAYER_SPEED
    player.clamp_ip((0, 0), (SCREEN_WIDTH, SCREEN_HEIGHT))
    for event in events:
        if event.type == KEYDOWN and event.dict['key'] == 32:    #スペースキーがそのフレームに押されたら
            character ^= 1  #キャラクターの絵柄を指定するbitを反転させる

def draw():
    screen.fill((0, 0, 0))
    screen.blit(player_image[character], player)  #player_imageの番号指定して絵柄切り替える

__init__()

'''
eventは識別番号(.typeで取得)と、辞書としてデータ(.dictで取得)を持つ
例えばスペースキーを押したとき、print(event.type, event.dict)
-> 768 {'unicode': ' ', 'key': 32, 'mod': 0, 'scancode': 44, 'window': None})>
768はKeyDownと対応、keyでどのキーが押されたか識別できる

pg.eventはqueue、pg.event.get()はdequeueと同じ操作なので
複数個所でイベント処理をしたいときは上のように配列にイベントを保存する必要がある
'''
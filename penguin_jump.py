'''必要なモジュールをimport'''
import pygame as pg
from pygame.locals import*
import sys
import random
import math

'''定数の設定'''
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_SPEED = 10
ENEMY_SPEED = 25
MAX_JUMP_POWER = 4650
GRAVITY = 5
FPS = 30

def main():
    '''pygameの実行、初期設定、ファイルの読み込み'''
    pg.init()
    screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    player_image_1 = pg.transform.smoothscale(pg.image.load("images/penguin_left.png").convert_alpha(), (80, 80))
    player_image_2 = pg.transform.smoothscale(pg.image.load("images/penguin_right.png").convert_alpha(), (80, 80))
    player_image_3 = pg.transform.smoothscale(pg.image.load("images/penguin_death.png").convert_alpha(), (80, 80))
    player_image = [player_image_1, player_image_2, player_image_3]
    enemy_image = pg.transform.smoothscale(pg.image.load("images/icicle.png").convert_alpha(), (80, 80))
    fish_image = pg.transform.smoothscale(pg.image.load("images/fish.png").convert_alpha(), (80, 80))
    font = pg.font.SysFont('meiryo', 55)

    '''変数の定義'''
    player = player_image[0].get_rect(x=350, y=520)
    player_dir = 'left'
    is_jumping = False
    jump_power = 0
    enemies = [enemy_image.get_rect(x=100*i, y=0) for i in range(8)]
    enemies_wait_time = [random.randint(30,210) for i in range(8)]
    player_alive = True
    fish = fish_image.get_rect(x=350, y=400)
    score = 0

    while True:
        events = [event for event in pg.event.get()]  #全てのイベントをeventsに保存

        '''ゲームの終了判定'''
        for event in events:
            if event.type == QUIT or pg.key.get_pressed()[K_ESCAPE]:
                return

        if player_alive:
            '''プレイヤーの座標の更新'''
            if pg.key.get_pressed()[K_a]:
                player.x = player.x - PLAYER_SPEED
                player_dir = 'left'
            elif pg.key.get_pressed()[K_d]:
                player.x = player.x + PLAYER_SPEED
                player_dir = 'right'
            if is_jumping:  #ジャンプしているとき
                jump_speed = jump_speed + GRAVITY  #速度の更新
                player.y = player.y + jump_speed  #座標の更新
            else:
                if pg.key.get_pressed()[K_SPACE]:  #スペースキーが押されているなら
                    jump_power += 190
                    jump_power = min(jump_power, MAX_JUMP_POWER)  #天井に当たらないようにする
                for event in events:
                    if event.type == KEYUP and event.dict['key'] == 32:  #スペースキーが離れたら
                        is_jumping = True
                        jump_speed = -math.sqrt(jump_power)  #初速度上向き
                        jump_power = 50
            if player.y > 520:
                player.y = 520
                is_jumping = False
            player.clamp_ip((0, 0), (SCREEN_WIDTH, SCREEN_HEIGHT))

            '''つららの座標の更新'''
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

            '''つららとの当たり判定'''
            for i in range(len(enemies)):  #if player.collidelistall(enemies) != []:(playerと接触しているenemies内のrectオブジェクトのindexを配列で返す)でもok
                if player.colliderect(enemies[i]):
                    player_alive = False

            '''魚との当たり判定'''
            if player.colliderect(fish):
                score = score + 1
                fish.x = random.randint(0, SCREEN_WIDTH-80)
                fish.y = random.randint(80, SCREEN_HEIGHT-80)

        elif pg.key.get_pressed()[K_r]:
            '''ゲームのリセット'''
            player = player_image[0].get_rect(x=350, y=520)
            player_dir = 'left'
            is_jumping = False
            jump_power = 0
            enemies = [enemy_image.get_rect(x=100*i, y=0) for i in range(8)]
            enemies_wait_time = [random.randint(30,210) for i in range(8)]
            player_alive = True
            fish = fish_image.get_rect(x=350, y=400)
            score = 0

        '''描画'''
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

        '''画面の切り替え、フレーム管理'''
        pg.display.update()
        pg.time.Clock().tick(FPS)

'''main関数を実行'''
main()
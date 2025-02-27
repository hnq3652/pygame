'''必要なモジュールをimport'''
import pygame as pg
from pygame.locals import*
import random

'''定数の設定'''
SCREEN_WIDTH = 380
SCREEN_HEIGHT = 560
PUYO_SPEED = 2  #ぷよのデフォルトの落下速度
FPS = 30

def main():
    '''pygameの実行、初期設定、ファイルの読み込み'''
    pg.init()
    screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    font = pg.font.SysFont("meiryo", 27)

    '''変数の定義'''
    array_dir = [[-40,40], [40,40], [40,-40], [-40,-40]]  #回転時の座標変化（[上から左, 左から下, ...]に対応)
    green_image = pg.transform.smoothscale(pg.image.load("images/緑.png").convert_alpha(), (40, 40))  #!
    blue_image = pg.transform.smoothscale(pg.image.load("images/青.png").convert_alpha(), (40, 40))  #!
    red_image = pg.transform.smoothscale(pg.image.load("images/赤.png").convert_alpha(), (40, 40))  #!
    yellow_image = pg.transform.smoothscale(pg.image.load("images/黄.png").convert_alpha(), (40, 40))  #!
    array_image = [green_image, blue_image, red_image, yellow_image]
    frame_count = 0
    wall_left = Rect((0,40), (40,480))  #左側の壁
    wall_right = Rect((280,40), (40,480))
    floor = Rect((0,520), (320,40))
    objects = [wall_left, wall_right, floor]  #当たり判定を調べるオブジェクト
    core_puyo = red_image.get_rect(x=120, y=40)  #ぷよは2つセットで
    connected_puyo = Rect((120,0), (40,40))
    core_color = random.randint(0,3)
    connected_color = random.randint(0,3)
    next_core_color = random.randint(0,3)
    next_connected_color = random.randint(0,3)
    direction = 0  #coreとconnectedの位置関係(最初はcoreの上にconnected)
    is_falling = True  #落下中かどうかのフラグ変数
    is_eliminated = True  #ぷよが消えるか調べるかどうかのフラグ変数
    wait_frame = 20  #ぷよが消える間隔
    chain = 0  #連鎖数
    graph_puyo = [[-1 for j in range(6)] for i in range(12)]  #ぷよを消す判定を調べるグラフ
    game_over = False

    while True:
        events = [event for event in pg.event.get()]
        frame_count += 1

        '''ゲームの終了判定'''
        for event in events:
            if event.type == QUIT or pg.key.get_pressed()[K_ESCAPE]:
                return

        if not game_over:
            if is_falling:  #ぷよが落下中なら
                '''ぷよの回転'''
                for event in events:
                    if event.type == KEYDOWN and event.dict['key'] == 119:  #Wが押されたなら
                        is_rotate = True  #回転をしたかのフラグ変数
                        connected_puyo.x += array_dir[direction][0]
                        connected_puyo.y += array_dir[direction][1]
                        if connected_puyo.collidelistall(objects) != []:  #回転させたぷよが他のobjectと当たるなら
                            if direction != 3:  #押し出し処理をするか判定
                                core_puyo[direction%2] -= array_dir[direction][direction%2]  #coreを押し出し
                                if core_puyo.collidelistall(objects) != []:  #coreを押し出しても他のものに当たるなら
                                    core_puyo[direction%2] += array_dir[direction][direction%2]  #もとの座標に戻す
                                    connected_puyo.x -= array_dir[direction][0]
                                    connected_puyo.y -= array_dir[direction][1]
                                    is_rotate = False
                                else:
                                    connected_puyo[direction%2] -= array_dir[direction][direction%2]  #coreの座標にconnectedを配置する
                        if is_rotate:
                            direction = (direction + 1)%4  #接続方向を更新する

                '''ぷよの落下'''
                ratio = 1
                if pg.key.get_pressed()[K_s]:
                    ratio = 10  #S押している間は落下速度10倍にする
                core_puyo.y += PUYO_SPEED*ratio
                connected_puyo.y += PUYO_SPEED*ratio
                if core_puyo.collidelistall(objects) != [] or connected_puyo.collidelistall(objects) != []:
                    core_puyo.y = core_puyo.y//40*40
                    connected_puyo.y = connected_puyo.y//40*40
                    is_falling = False

                    '''ぷよの切り離し'''
                    if direction == 1 or direction == 3:
                        while core_puyo.collidelistall(objects) == []:  #真下に他の物がない間y座標を増やす
                            core_puyo.y += 40
                        core_puyo.y -= 40
                        while connected_puyo.collidelistall(objects) == []:
                            connected_puyo.y += 40
                        connected_puyo.y -= 40
                    objects.append(core_puyo)  #objectsを更新
                    objects.append(connected_puyo)
                    graph_puyo[core_puyo.y//40 - 1][core_puyo.x//40 - 1] = core_color  #graph_puyoを更新
                    graph_puyo[connected_puyo.y//40 - 1][connected_puyo.x//40 - 1] = connected_color

                '''ぷよの横移動'''
                for event in events:
                    dx = 0
                    if event.type == KEYDOWN and event.dict['key'] == 97:
                        dx = -40
                    if event.type == KEYDOWN and event.dict['key'] == 100:
                        dx = 40
                    core_puyo.x += dx
                    connected_puyo.x += dx
                    if core_puyo.collidelistall(objects) != [] or connected_puyo.collidelistall(objects) != []:
                        core_puyo.x -= dx
                        connected_puyo.x -= dx

            else:
                wait_frame -= 1
                if wait_frame == 0:  #20フレーム待つ
                    if is_eliminated:
                        is_eliminated = False
                        wait_frame = 20
                        '''同じ色のぷよが4つ以上繋がっているかbfsで判定'''
                        for i in range(12):
                            for j in range(6):
                                if graph_puyo[i][j] != -1:
                                    color = graph_puyo[i][j]
                                    stack = [(i,j)]
                                    is_checked = [(i,j)]
                                    while stack != []:
                                        now_i,now_j = stack.pop()
                                        for di,dj in [[-1,0],[1,0],[0,-1],[0,1]]:
                                            if 0 <= now_i+di < 12 and 0 <= now_j+dj < 6:
                                                if graph_puyo[now_i+di][now_j+dj] == color and not (now_i+di,now_j+dj) in is_checked:
                                                    stack.append((now_i+di,now_j+dj))
                                                    is_checked.append((now_i+di,now_j+dj))
                                    if len(is_checked) >= 4:
                                        if not is_eliminated:
                                            chain += 1
                                            is_eliminated = True
                                        for k,l in is_checked:
                                            graph_puyo[k][l] = -1

                        '''ぷよを落下させる処理'''
                        for j in range(6):
                            stack = [-1 for i in range(12)]
                            for i in range(12):
                                if graph_puyo[i][j] != -1:
                                    stack.append(graph_puyo[i][j])  #上からぷよをstackに入れる
                            for i in range(11,-1,-1):
                                graph_puyo[i][j] = stack.pop()  #下からstackの中身を戻す
                        objects = objects[:3]  #objectsをgraph_puyoから再構築する
                        for i in range(12):
                            for j in range(6):
                                if graph_puyo[i][j] != -1:
                                    objects.append(Rect((40*(j+1),40*(i+1)), (40,40)))
                    else:  #ぷよが消えなくなったら
                        if graph_puyo[0][2] != -1:  #出現地点にぷよがあったら
                            game_over = True

                        else:
                            '''次のぷよの生成'''
                            core_puyo = Rect((120,40), (40,40))
                            connected_puyo = Rect((120,0), (40,40))
                            core_color = next_core_color
                            connected_color = next_connected_color
                            next_core_color = random.randint(0,3)
                            next_connected_color = random.randint(0,3)
                            direction = 0
                            is_falling = True
                            wait_frame = 20
                            is_eliminated = True
                            chain = 0

        else:  #ゲームオーバーのとき
            if pg.key.get_pressed()[K_r]:  #R押したらリセット
                frame_count = 0
                objects = [wall_left, wall_right, floor]
                core_puyo = Rect((120,40), (40,40))
                connected_puyo = Rect((120,0), (40,40))
                core_color = random.randint(0,3)
                connected_color = random.randint(0,3)
                next_core_color = random.randint(0,3)
                next_connected_color = random.randint(0,3)
                direction = 0
                is_falling = True
                is_eliminated = True
                chain = 0
                graph_puyo = [[-1 for j in range(6)] for i in range(12)]
                game_over = False

        '''描画'''
        screen.fill((0, 0, 0))
        for i in range(3):
            pg.draw.rect(screen, (255,255,255), objects[i])
        for i in range(12):
            for j in range(6):
                if graph_puyo[i][j] != -1:
                    screen.blit(array_image[graph_puyo[i][j]], Rect((40*(j+1),40*(i+1)), (40,40)))
        if chain >= 2:
            screen.blit(font.render(f'{chain}れんさ', True, (0, 0, 0)), (110,520))
        if is_falling:
            screen.blit(array_image[core_color], core_puyo)
            screen.blit(array_image[connected_color], connected_puyo)
        pg.draw.rect(screen, next_core_color, Rect((330,120), (40,40)))
        pg.draw.rect(screen, next_connected_color, Rect((330,80), (40,40)))
        if game_over:
            screen.blit(font.render(f'おわり', True, (255, 255, 255)), (110,200))
            screen.blit(font.render(f'Rでリセット', True, (255, 255, 255)), (100,230))

        pg.display.flip()
        pg.time.Clock().tick(FPS)

main()
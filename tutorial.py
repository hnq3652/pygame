import pygame as pg  #pygameモジュールをインポートする
from pygame.locals import*  #pygameモジュールの定数をインポートする(event.type: QUITなど)

SCREEN_WIDTH = 800  #画面の横幅を定数にする
SCREEN_HEIGHT = 600  #画面の縦幅
PLAYER_SPEED = 5  #プレイヤーのスピード
FPS = 30  #フレームレート

def __init__():  #ゲームの初期設定をする関数を定義する
    global screen, player_image, player, enemy, player_alive, message  #全ての変数をグローバル化
    pg.init()  #pygameを初期化?実行?する
    screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  #画面サイズを横800、縦600にする
    player_image = pg.transform.smoothscale(pg.image.load("images/robonyan.png").convert_alpha(), (60, 60))  #プレイヤーの画像を読み込んで(60,60)の大きさに調整する
    player = player_image.get_rect(x=0, y=200)  #プレイヤーを位置(0,200)の長方形にする
    enemy = Rect((500, 500), (60, 60))
    player_alive = True  #プレイヤーが生きているかのフラグ変数(最初は生きているのでTrue)
    font = pg.font.Font(None, 60)  #フォントを設定する
    message = font.render('GAME OVER', True, (255, 255, 255))  #死亡時に表示するメッセージ(文字列,アンチエイリアス,色)を設定する
    while True:  #ずっと繰り返す
        update()  #プレイヤーの座標など、動きの更新の関数を実行する
        draw()  #描画の関数を実行する
        pg.display.update()  #更新した画面に切り替える(絵が二枚できたら次の絵にいけるよねーのイメージ)
        for event in pg.event.get():  #イベント処理(ゲーム(プログラム)の終了、フルスクリーン切り替えなど)
            if event.type == QUIT or pg.key.get_pressed()[K_ESCAPE]:  #画面の×ボタンが押されるか、escapeキーが押されたら
                return  #プログラムを終了する(ゲーム終了)
        pg.time.Clock().tick(FPS)  #30FPSで動くように調整する

def update():  #動き(プレイヤーの座標など)の更新をする関数を定義する
    if player_alive:  #もしプレイヤーが生きているなら
        update_player()  #プレイヤーの座標の更新
        update_enemy()  #敵の座標の更新
        check_collision()  #当たり判定の更新

def update_player():
    global player  #プレイヤーをグローバル化
    if pg.key.get_pressed()[K_w]:  #もしWが押されたら(長押し可能)
        player.y = player.y - PLAYER_SPEED  #プレイヤーのy座標を5減らす(上に5動く)
    elif pg.key.get_pressed()[K_s]:
        player.y = player.y + PLAYER_SPEED  #プレイヤーのy座標を5増やす(下に5動く)
    if pg.key.get_pressed()[K_a]:
        player.x = player.x - PLAYER_SPEED  #プレイヤーのx座標を5減らす(左に5動く)
    elif pg.key.get_pressed()[K_d]:
        player.x = player.x + PLAYER_SPEED  #プレイヤーのx座標を5増やす(右に5動く)
    player.clamp_ip((0, 0), (SCREEN_WIDTH, SCREEN_HEIGHT))  #プレイヤーが(0,0)から(800,600)の範囲から出ないようにする

def update_enemy():
    global enemy  #敵をグローバル化
    enemy.x = enemy.x - 10  #敵を左に10動かす
    if enemy.x < -60:  #画面左側で見切れたら
        enemy.x = SCREEN_WIDTH  #画面右側に戻す

def check_collision():
    global player_alive
    if player.colliderect(enemy):  #もしplayerがenemyに接触しているなら
        player_alive = False  #プレイヤーが生きていない状態にする

def draw():  #描画をする関数を定義する
    screen.fill((0, 0, 0))  #画面を黒色(カラーコード:000000)で塗りつぶす
    if player_alive:
        screen.blit(player_image, player)  #player_imageをplayerの位置に配置する
        pg.draw.rect(screen, (0,255,255), enemy)  #水色の四角(敵)を配置する
    else:
        screen.blit(message, (300,280))  #指定した座標に文字を配置する

__init__()  #プログラムを実行する
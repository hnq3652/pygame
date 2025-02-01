import pygame as pg  #pygameモジュールをインポートする
from pygame.locals import*  #pygameモジュールの定数をインポートする(event.type: QUITなど)

def __init__():  #ゲームの初期設定をする関数を定義する
    global screen, player_color, player  #画面、プレイヤーの色、プレイヤーをグローバル化
    pg.init()  #pygameを初期化?実行?する
    screen = pg.display.set_mode((800, 600))  #画面サイズを横800、縦600にする
    player_color = (0, 255, 255)  #プレイヤーの色を水色(カラーコード:00ffff)にする
    player = Rect((0, 200), (60, 60))  #プレイヤーを座標(x,y)=(0,200)、(横,縦)=(60,60)の長方形にする
    while True:  #ずっと繰り返す
        update()  #プレイヤーの座標など、動きの更新の関数を実行する
        draw()  #描画の関数を実行する
        pg.display.update()  #更新した画面に切り替える(絵が二枚できたら次の絵にいけるよねーのイメージ)
        for event in pg.event.get():  #イベント処理(ゲーム(プログラム)の終了、フルスクリーン切り替えなど)
            if event.type == QUIT or pg.key.get_pressed()[K_ESCAPE]:  #画面の×ボタンが押されるか、escapeキーが押されたら
                return  #プログラムを終了する(ゲーム終了)
        pg.time.Clock().tick(30)  #30FPSで動くように調整する

def update():  #動き(プレイヤーの座標など)の更新をする関数を定義する
    global player  #プレイヤーをグローバル化
    player.x = player.x + 5  #プレイヤーのx座標を5増やす(右に5動く)
    if player.x > 800:  #もしx座標が画面の横幅より大きいなら(画面右側で見切れたら)
        player.x = 0  #x座標を0にする

def draw():  #描画をする関数を定義する
    screen.fill((0, 0, 0))  #画面を黒色(カラーコード:000000)で塗りつぶす
    pg.draw.rect(screen, player_color, player)  #screenに、水色の、プレイヤーを配置する

__init__()  #プログラムを実行する
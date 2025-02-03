'''必要なモジュールをimport'''
import pygame as pg  #pygameモジュールをインポートする
from pygame.locals import*  #pygameモジュールの定数をインポートする(event.type: QUITなど)

'''定数の設定'''
SCREEN_WIDTH = 800  #画面の横幅を定数にする
SCREEN_HEIGHT = 600  #画面の縦幅
PLAYER_SPEED = 5  #プレイヤーのスピード
FPS = 30  #フレームレート

def main():  #ゲームの初期設定をする関数を定義する
    '''pygameの実行、初期設定、ファイルの読み込み'''
    pg.init()  #pygameを初期化?実行?する
    screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  #画面サイズを横800、縦600にする
    player_image = pg.transform.smoothscale(pg.image.load("images/robonyan.png").convert_alpha(), (60, 60))  #プレイヤーの画像を読み込んで(60,60)の大きさに調整する
    font = pg.font.Font(None, 60)  #フォントを設定する  #画像の読み込みやフォントの設定

    '''変数の定義'''
    player = player_image.get_rect(x=0, y=200)  #プレイヤーを位置(0,200)の長方形にする
    enemy = Rect((500, 500), (60, 60))
    player_alive = True  #プレイヤーが生きているかのフラグ変数(最初は生きているのでTrue)

    while True:  #ずっと繰り返す
        '''ゲームの終了判定'''
        for event in pg.event.get():  #イベント処理(ゲーム(プログラム)の終了、フルスクリーン切り替えなど)
            if event.type == QUIT or pg.key.get_pressed()[K_ESCAPE]:  #画面の×ボタンが押されるか、escapeキーが押されたら
                return  #プログラムを終了する(ゲーム終了)

        if player_alive:  #もしプレイヤーが生きているなら
            '''プレイヤーの座標の更新'''
            if pg.key.get_pressed()[K_w]:  #もしWが押されたら(長押し可能)
                player.y = player.y - PLAYER_SPEED  #プレイヤーのy座標を5減らす(上に5動く)
            elif pg.key.get_pressed()[K_s]:
                player.y = player.y + PLAYER_SPEED  #プレイヤーのy座標を5増やす(下に5動く)
            if pg.key.get_pressed()[K_a]:
                player.x = player.x - PLAYER_SPEED  #プレイヤーのx座標を5減らす(左に5動く)
            elif pg.key.get_pressed()[K_d]:
                player.x = player.x + PLAYER_SPEED  #プレイヤーのx座標を5増やす(右に5動く)
            player.clamp_ip((0, 0), (SCREEN_WIDTH, SCREEN_HEIGHT))  #プレイヤーが(0,0)から(800,600)の範囲から出ないようにする

            '''敵の座標の更新'''
            enemy.x = enemy.x - 10  #敵を左に10動かす
            if enemy.x < -60:  #画面左側で見切れたら
                enemy.x = SCREEN_WIDTH  #画面右側に戻す

            '''当たり判定'''
            if player.colliderect(enemy):  #もしplayerがenemyに接触しているなら
                player_alive = False  #プレイヤーが生きていない状態にする

        else:  #もしプレイヤーが死んでいるなら
            if pg.key.get_pressed()[K_SPACE]:  #もしスペースキーが押されたら
                '''ゲームのリセット'''
                player = player_image.get_rect(x=0, y=200)  #プレイヤーを位置(0,200)の長方形にする
                enemy = Rect((500, 500), (60, 60))
                player_alive = True  #プレイヤーが生きているかのフラグ変数(最初は生きているのでTrue)

        '''描画'''
        screen.fill((0, 0, 0))  #画面を黒色(カラーコード:000000)で塗りつぶす
        if player_alive:
            screen.blit(player_image, player)  #player_imageをplayerの位置に配置する
            pg.draw.rect(screen, (0,255,255), enemy)  #水色の四角(敵)を配置する
        else:
            message = font.render('press space to continue', True, (255, 255, 255))  #死亡時に表示するメッセージ(文字列,アンチエイリアス,色)を設定する
            screen.blit(message, (150,280))  #指定した座標に文字を配置する

        '''画面の切り替え、フレーム管理'''
        pg.display.update()  #更新した画面に切り替える(絵が二枚できたら次の絵にいけるよねーのイメージ)
        pg.time.Clock().tick(FPS)  #30FPSで動くように調整する

'''main関数を実行'''
main()  #プログラムを実行する
import pygame as pg
from pygame.locals import*

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_SPEED = 5
FPS = 30

def main():
    pg.init()
    screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    player_image = pg.transform.smoothscale(pg.image.load("images/robonyan.png").convert_alpha(), (60, 60))
    font = pg.font.Font(None, 60)

    player = player_image.get_rect(x=0, y=200)
    enemy = Rect((500, 500), (60, 60))
    player_alive = True

    while True:
        for event in pg.event.get():
            if event.type == QUIT or pg.key.get_pressed()[K_ESCAPE]:
                return

        if player_alive:
            if pg.key.get_pressed()[K_w]:
                player.y = player.y - PLAYER_SPEED
            elif pg.key.get_pressed()[K_s]:
                player.y = player.y + PLAYER_SPEED
            if pg.key.get_pressed()[K_a]:
                player.x = player.x - PLAYER_SPEED
            elif pg.key.get_pressed()[K_d]:
                player.x = player.x + PLAYER_SPEED
            player.clamp_ip((0, 0), (SCREEN_WIDTH, SCREEN_HEIGHT))

            enemy.x = enemy.x - 10
            if enemy.x < -60:
                enemy.x = SCREEN_WIDTH

            if player.colliderect(enemy):
                player_alive = False

        else:
            if pg.key.get_pressed()[K_SPACE]:
                player = player_image.get_rect(x=0, y=200)
                enemy = Rect((500, 500), (60, 60))
                player_alive = True

        screen.fill((0, 0, 0))
        if player_alive:
            screen.blit(player_image, player)
            pg.draw.rect(screen, (0,255,255), enemy)
        else:
            message = font.render('press space to continue', True, (255, 255, 255))
            screen.blit(message, (150,280))

        pg.display.update()
        pg.time.Clock().tick(FPS)

main()
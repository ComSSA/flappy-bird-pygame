import pygame

import assets
import configs
from objects.background import Background
from objects.bird import Bird
from objects.column import Column
from objects.floor import Floor
from objects.gameover_message import GameOverMessage
from objects.gamestart_message import GameStartMessage
from objects.score import Score

pygame.init()

screen = pygame.display.set_mode((configs.SCREEN_WIDTH, configs.SCREEN_HEIGHT))

pygame.display.set_caption("Flappy Bird Game v1.1 COMSSA Edition")

img = pygame.image.load('assets/icons/red_bird.png')
pygame.display.set_icon(img)


clock = pygame.time.Clock()
column_create_event = pygame.USEREVENT
death_timer_event = pygame.USEREVENT + 1

running = True
gameover = False
gamestarted = False

gameDeathWait = False

assets.load_sprites()
assets.load_audios()

sprites = pygame.sprite.LayeredUpdates()


def create_sprites():
    Background(0, sprites)
    Background(1, sprites)
    Floor(0, sprites)
    Floor(1, sprites)

    return Bird(sprites), GameStartMessage(sprites), Score(sprites)


bird, game_start_message, score = create_sprites()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == column_create_event:
            Column(sprites)
        if event.type == death_timer_event:
            gameDeathWait = False

        if not gameover:
            bird.handle_event(event)
        

        if (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE) or (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1): # Space bar or Left Mouse click
            if not gamestarted and not gameover:
                gamestarted = True
                game_start_message.kill()
                pygame.time.set_timer(column_create_event, 1500)
            if gameover and not gameDeathWait:
                gameover = False
                gamestarted = False
                sprites.empty()
                bird, game_start_message, score = create_sprites()

    screen.fill(0)

    sprites.draw(screen)

    if gamestarted and not gameover:
        sprites.update()

    if bird.check_collision(sprites) and not gameover:
        gameover = True
        gamestarted = False
        GameOverMessage(sprites)
        pygame.time.set_timer(column_create_event, 0)
        assets.play_audio("hit")
        gameDeathWait = True
        print("Game ended with score of:", score.value)
        pygame.time.set_timer(death_timer_event, 1000) # 1 second wait before allowed to replay game

    for sprite in sprites:
        if type(sprite) is Column and sprite.is_passed():
            score.value += 1
            assets.play_audio("point")

    pygame.display.flip()
    clock.tick(configs.FPS)

pygame.quit()

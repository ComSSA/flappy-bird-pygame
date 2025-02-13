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

infoSize = pygame.display.Info()
screen = pygame.display.set_mode((infoSize.current_w, infoSize.current_h), pygame.RESIZABLE)


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
        if event.type == pygame.VIDEORESIZE: # Resize event
            width, height = event.size
            if width < configs.GAME_WIDTH:
                width = configs.GAME_WIDTH
            if height < configs.GAME_HEIGHT:
                height = configs.GAME_HEIGHT
            screen = pygame.display.set_mode((width,height), pygame.RESIZABLE)
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

    screen.fill(pygame.Color(68,89,165))

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

    # Draw mask
    pygame.draw.rect(screen, pygame.Color(68,89,165), pygame.Rect(0,0, configs.getGameArea().left, configs.getGameArea().centery * 2))
    pygame.draw.rect(screen, pygame.Color(68,89,165), pygame.Rect(configs.getGameArea().left,0, configs.getGameArea().width, configs.getGameArea().top))
    pygame.draw.rect(screen, pygame.Color(68,89,165), pygame.Rect(configs.getGameArea().right,0, configs.getGameArea().left, configs.getGameArea().centery * 2))
    pygame.draw.rect(screen, pygame.Color(68,89,165), pygame.Rect(configs.getGameArea().left,configs.getGameArea().bottom, configs.getGameArea().width, configs.getGameArea().top))


    pygame.display.flip()
    clock.tick(configs.FPS)

pygame.quit()

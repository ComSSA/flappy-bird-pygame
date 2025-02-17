from objects.text import GameText
import pygame

import assets
import configs
from objects.background import Background
from objects.bird import Bird
from objects.column import Column
from objects.floor import Floor
from objects.gameover_message import GameOverMessage
from objects.gamestart_message import GameStartMessage
from objects.leaderboard import Leaderboard
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
show_leaderboard = False
leaderboard = Leaderboard()
leaderboard_score = [leaderboard.get_leaderboard()[i][1] for i in range(len(leaderboard.get_leaderboard()))]

gameDeathWait = False

assets.load_sprites()
assets.load_audios()

sprites = pygame.sprite.LayeredUpdates()

def top_3_leaderboard_text():
    top_3_leaderboard = leaderboard.read_top_3_leaderboard()
    top_3_leadboard_text = [GameText(f"{i+1}. {top_3_leaderboard[i][0].get_user_info()[0]} - {top_3_leaderboard[i][1]}", 30, (screen.get_width() - configs.getGameArea().right / 3, configs.getGameArea().centery - 40 + (35 * i))) for i in range(len(top_3_leaderboard))]
    return top_3_leadboard_text

def create_sprites():
    Background(0, sprites)
    Background(1, sprites)
    Floor(0, sprites)
    Floor(1, sprites)
    return Bird(sprites), GameStartMessage(sprites), Score(sprites)

bird, game_start_message, score = create_sprites()
top_3_leaderboard = leaderboard.read_top_3_leaderboard()

control_text = GameText("Controls", 36, (configs.getGameArea().left / 2, configs.getGameArea().centery - 80))
space_text = GameText("Space or Left Click to Start", 30, (configs.getGameArea().left / 2, configs.getGameArea().centery))
leaderboard_text = GameText("Press L for Leaderboard", 30, (configs.getGameArea().left / 2, configs.getGameArea().centery + 50))
good_luck_text = GameText("Good Luck! ^_^", 34, (configs.getGameArea().left / 2, configs.getGameArea().centery + 110))


# Top 3 Leaderboard
top_3_leaderboard_title = GameText("Top 3 Leaderboard", 36, (screen.get_width() - configs.getGameArea().right / 3, configs.getGameArea().centery - 110))
top_3_leadboard_text = top_3_leaderboard_text()

# Prize title
prize_title_text = GameText("Prizes", 36, (screen.get_width() - configs.getGameArea().right / 3, configs.getGameArea().centery + 100))
prize_list = ["Steam Voucher", "ComSSA Hat", "ComSSA Bottle"]
prize_text = [GameText(f"{i+1}. {prize_list[i]}", 30, (screen.get_width() - configs.getGameArea().right / 3, configs.getGameArea().centery + 150 + (35 * i))) for i in range(len(prize_list))]
# scale down logo image
logo_image = assets.get_sprite("ComSSALogo")
original_size = logo_image.get_size()
scale_factor = 0.5
new_width = int(original_size[0] * scale_factor)
new_height = int(original_size[1] * scale_factor)
logo_image = pygame.transform.scale(logo_image, (new_width, new_height))
logo_rect = logo_image.get_rect(center=(screen.get_width() - configs.getGameArea().right / 3, configs.getGameArea().top - 20))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == column_create_event:
            Column(sprites, score=score.value)
        if event.type == pygame.VIDEORESIZE: # Resize event
            width, height = event.size
            if width < configs.GAME_WIDTH:
                width = configs.GAME_WIDTH
            if height < configs.GAME_HEIGHT:
                height = configs.GAME_HEIGHT
            screen = pygame.display.set_mode((width,height), pygame.RESIZABLE)

            # update text positions
            control_text.update((configs.getGameArea().left / 2, configs.getGameArea().centery - 80))
            space_text.update((configs.getGameArea().left / 2, configs.getGameArea().centery))
            leaderboard_text.update((configs.getGameArea().left / 2, configs.getGameArea().centery + 50))
            good_luck_text.update((configs.getGameArea().left / 2, configs.getGameArea().centery + 110))
            top_3_leaderboard_title.update((screen.get_width() - configs.getGameArea().right / 3, configs.getGameArea().centery - 110))
            logo_rect = logo_image.get_rect(center=(screen.get_width() - configs.getGameArea().right / 3, configs.getGameArea().top - 20))
            prize_title_text.update((screen.get_width() - configs.getGameArea().right / 3, configs.getGameArea().centery + 100))
            for i in range(len(top_3_leadboard_text)):
                top_3_leadboard_text[i].update((screen.get_width() - configs.getGameArea().right / 3, configs.getGameArea().centery - 40 + (35 * i)))
            for i in range(len(prize_text)):
                prize_text[i].update((screen.get_width() - configs.getGameArea().right / 3, configs.getGameArea().centery + 150 + (35 * i)))
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
                if not leaderboard.is_active:
                    leaderboard.fill_leaderboard(screen, score.value)
                    top_3_leadboard_text = top_3_leaderboard_text()
                    gameover = False
                    gamestarted = False
                    sprites.empty()
                    bird, game_start_message, score = create_sprites()

        if (event.type == pygame.KEYDOWN and event.key == pygame.K_l):
            if not gamestarted:
                if not leaderboard.is_active:
                    leaderboard.draw_leaderboard(screen)

    screen.fill(configs.COMSSA_COLOR)

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
        pygame.time.set_timer(death_timer_event, 200) # 0.2 second wait before allowed to replay game

    for sprite in sprites:
        if type(sprite) is Column and sprite.is_passed():
            score.value += 1
            assets.play_audio("point")

    # Draw mask
    pygame.draw.rect(screen, configs.COMSSA_COLOR, pygame.Rect(0,0, configs.getGameArea().left, configs.getGameArea().centery * 2))
    pygame.draw.rect(screen, configs.COMSSA_COLOR, pygame.Rect(configs.getGameArea().left,0, configs.getGameArea().width, configs.getGameArea().top))
    pygame.draw.rect(screen, configs.COMSSA_COLOR, pygame.Rect(configs.getGameArea().right,0, configs.getGameArea().left, configs.getGameArea().centery * 2))
    pygame.draw.rect(screen, configs.COMSSA_COLOR, pygame.Rect(configs.getGameArea().left,configs.getGameArea().bottom, configs.getGameArea().width, configs.getGameArea().top))

    control_text.draw(screen)
    space_text.draw(screen)
    leaderboard_text.draw(screen)
    good_luck_text.draw(screen)
    prize_title_text.draw(screen)
    # Top 3 Leaderboard
    top_3_leaderboard_title.draw(screen)
    for text in top_3_leadboard_text:
        text.draw(screen)

    # Prizes
    for text in prize_text:
        text.draw(screen)

    screen.blit(logo_image, logo_rect)

    pygame.display.flip()
    clock.tick(configs.FPS)

pygame.quit()



import pygame

GAME_WIDTH = 288
GAME_HEIGHT = 512
FPS = 60
GRAVITY = 0.4
COMSSA_COLOR = (68,89,165)

def getGameArea():
    w, h = pygame.display.get_surface().get_size()
    return pygame.Rect(w / 2 - GAME_WIDTH / 2, h / 2 - GAME_HEIGHT / 2, GAME_WIDTH, GAME_HEIGHT)
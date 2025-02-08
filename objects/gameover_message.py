import pygame.sprite

import assets
import configs
from layer import Layer


class GameOverMessage(pygame.sprite.Sprite):
    def __init__(self, *groups):
        self._layer = Layer.UI
        self.image = assets.get_sprite("gameover")
        self.rect = self.image.get_rect(center=configs.getGameArea().center)
        super().__init__(*groups)

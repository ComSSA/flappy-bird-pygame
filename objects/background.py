import pygame.sprite

import assets
import configs
from layer import Layer


class Background(pygame.sprite.Sprite):
    def __init__(self, index, *groups):
        self._layer = Layer.BACKGROUND
        self.image = assets.get_sprite("background")
        self.rect = self.image.get_rect(topleft=(configs.GAME_WIDTH * index + configs.getGameArea().left, configs.getGameArea().top))

        super().__init__(*groups)

    def update(self):
        self.rect.x -= 1

        if self.rect.right <= configs.getGameArea().left:
            self.rect.x = configs.getGameArea().right

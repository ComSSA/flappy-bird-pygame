import pygame.sprite

import assets
import configs
from layer import Layer


class Floor(pygame.sprite.Sprite):
    def __init__(self, index, *groups):
        self._layer = Layer.FLOOR
        self.image = assets.get_sprite("floor")
        self.rect = self.image.get_rect(bottomleft=(configs.GAME_WIDTH * index + configs.getGameArea().left, configs.getGameArea().bottom))
        self.mask = pygame.mask.from_surface(self.image)
        super().__init__(*groups)

    def update(self):
        self.rect.x -= 2

        if self.rect.right <= configs.getGameArea().left:
            self.rect.x = configs.getGameArea().right

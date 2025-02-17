import random

import pygame.sprite

import assets
import configs
from layer import Layer


class Column(pygame.sprite.Sprite):
    def __init__(self, *groups, score):
        self._layer = Layer.OBSTACLE

        self.gap = 80 + random.randint(int(max(0, 15 - score)), int(max(0, min(60, 70 - 3 * score)))) # Add randomness to gap which gets harder over time, hardest at score 24

        self.sprite = assets.get_sprite("pipe-green")
        self.sprite_rect = self.sprite.get_rect()

        self.pipe_bottom = self.sprite
        self.pipe_bottom_rect = self.pipe_bottom.get_rect(topleft=(0, self.sprite_rect.height + self.gap))

        self.pipe_top = pygame.transform.flip(self.sprite, False, True)
        self.pipe_top_rect = self.pipe_top.get_rect(topleft=(0, 0))

        self.image = pygame.surface.Surface((self.sprite_rect.width, self.sprite_rect.height * 2 + self.gap),
                                            pygame.SRCALPHA)
        self.image.blit(self.pipe_bottom, self.pipe_bottom_rect)
        self.image.blit(self.pipe_top, self.pipe_top_rect)

        sprite_floor_height = assets.get_sprite("floor").get_rect().height
        min_y = configs.getGameArea().top + 100
        max_y = configs.getGameArea().bottom - sprite_floor_height - 100

        self.rect = self.image.get_rect(midleft=(configs.getGameArea().right, random.uniform(min_y, max_y)))
        self.mask = pygame.mask.from_surface(self.image)

        self.passed = False

        super().__init__(*groups)

    def update(self):
        self.rect.x -= 2

        if self.rect.right <= configs.getGameArea().left:
            self.kill()

    def is_passed(self):
        if self.rect.x < configs.getGameArea().left + 50 and not self.passed:
            self.passed = True
            return True
        return False

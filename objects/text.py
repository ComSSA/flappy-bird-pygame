import pygame


class GameText:
    def __init__(self, text, size, position):
        self.text = text
        self.size = size
        self.position = position
        self.text_surface = None
        self.text_rect = None

        # Make as another function so this doesn't look like inside a constructor
        self.setup()

    def setup(self):
        font = pygame.font.Font('assets/fonts/BlackOpsOne-Regular.ttf', self.size)
        self.text_surface = font.render(self.text, True, (255, 255, 255))
        self.text_rect = self.text_surface.get_rect()
        self.text_rect.center = self.position

    def draw(self, surface):
        # Make sure that the text surface and text rect are setup (not needed but just in case the setup function has errors)
        if self.text_surface is not None and self.text_rect is not None:
            surface.blit(self.text_surface, self.text_rect)

    def update(self, position):
        self.text_rect = self.text_surface.get_rect()
        self.text_rect.center = position
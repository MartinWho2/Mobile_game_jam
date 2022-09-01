import pygame


class Text:
    def __init__(self, coo, text, tile_size):
        self.coo = coo
        self.text = text
        self.font = self.font = pygame.font.SysFont('arial', 30)
        self.image = self.font.render(self.text, True, (0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = self.coo[0] * tile_size, self.coo[1] * tile_size



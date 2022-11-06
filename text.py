import pygame


class Text:
    def __init__(self, coo, text, tile_size,path):
        self.coo = coo
        self.text = text
        self.font = self.font = pygame.font.Font(path + 'media/fonts/pixel-font.ttf', 13)
        self.image = self.font.render(self.text, True, "white")
        self.rect = self.image.get_rect()
        self.rect.center = self.coo[0] * tile_size, self.coo[1] * tile_size



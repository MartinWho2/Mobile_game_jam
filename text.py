import pygame


class Text:
    def __init__(self, coo, text, tile_size,path):
        self.coo = coo
        self.text = text
        self.font = self.font = pygame.font.Font(path + 'media/fonts/pixel-font.ttf', 13)
        self.image_white = self.font.render(self.text, True, "white")
        self.image_black = self.font.render(self.text, True, "black")
        offset = 0.1
        self.image = pygame.surface.Surface((self.image_black.get_width()*(1+offset),self.image_black.get_height()*(1+offset)),
                                            pygame.SRCALPHA)
        self.image.blit(self.image_black,(self.image_black.get_height()*offset,self.image_black.get_height()*offset))
        self.image.blit(self.image_white,(0,0))
        self.rect = self.image.get_rect()
        self.rect.center = self.coo[0] * tile_size, self.coo[1] * tile_size



import pygame


class Button(pygame.sprite.Sprite):
    def __init__(self, path, coo, group, tile_size):
        super().__init__()
        self.image = pygame.image.load(path + 'media/button_on.png').convert_alpha()
        self.image_off = pygame.image.load(path + 'media/button_off.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = coo[0] * tile_size
        self.rect.y = coo[1] * tile_size
        self.group = group
        self.tile_size = tile_size


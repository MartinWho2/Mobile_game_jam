import pygame


class Button(pygame.sprite.Sprite):
    def __init__(self, path, coo, num, tile_size):
        super().__init__()
        self.image_on = pygame.image.load(path + 'media/button_on.png').convert_alpha()
        self.image_off = pygame.image.load(path + 'media/button_off.png').convert_alpha()
        self.rect = self.image_on.get_rect()
        self.rect.x = coo[0] * tile_size
        self.rect.y = coo[1] * tile_size
        self.num = num
        self.tile_size = tile_size
        self.on = False
        self.images = {True: self.image_on, False: self.image_off}
        self.image = self.images[self.on]

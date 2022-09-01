import pygame


class Vent(pygame.sprite.Sprite):
    def __init__(self, path, coo, dest, group, tile_size, turned=False):
        super().__init__()
        self.tile_size = tile_size
        self.image = pygame.image.load(path + 'media/vent.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = coo[0]*self.tile_size
        self.rect.y = coo[1]*self.tile_size
        self.group = group
        self.dest = dest[0]*self.tile_size, dest[1]*self.tile_size

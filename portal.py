import pygame


class Portal(pygame.sprite.Sprite):
    def __init__(self, path, infos, tile_size):
        super().__init__()
        self.tile_size = tile_size
        self.image = pygame.image.load(path + 'media/portal.png').convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = infos[0] * tile_size
        self.rect.y = infos[1] * tile_size
        self.type = infos[2]

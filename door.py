import pygame


class Door(pygame.sprite.Sprite):
    def __init__(self, path, coo, num, tile_size, opened=False, turned=False):
        super().__init__()
        self.tile_size = tile_size
        if turned:
            self.image = pygame.transform.rotate(pygame.image.load(path + 'media/new_door.png').convert_alpha(),90)
        else:
            self.image = pygame.image.load(path + 'media/new_door.png').convert_alpha()

        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = coo[0] * tile_size
        self.rect.y = coo[1] * tile_size
        self.num = num
        self.opened = opened


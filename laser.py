import pygame


class Laser(pygame.sprite.Sprite):
    def __init__(self, pos, direction: str, tile_size, path):  # Image to be inputted with full path
        super().__init__()
        self.pos = pos
        self.directions = {'left': True, 'right': False, direction: True}
        self.tower_image = pygame.transform.scale(pygame.image.load(path + 'media/laser.png').convert_alpha(),
                                                  (tile_size, tile_size))
        self.tower_rect = self.tower_image.get_rect()
        self.tower_rect.topleft = pos
        self.laser_image = pygame.transform.scale(pygame.image.load(path + 'media/laser.png').convert_alpha(),
                                                  (tile_size, tile_size))

        
    def blit_tower(self, window: pygame.Surface):
        window.blit(self.tower_image, self.tower_rect)
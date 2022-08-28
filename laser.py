import pygame


class Tower(pygame.sprite.Sprite):
    def __init__(self, path, pos: tuple, direction, tile_size, tiles):  # Image to be inputted with full path
        super().__init__()
        self.pos = pos
        self.path = path
        if direction in {"left", "right"}:
            image_name = 'media/turret.png'
        else:
            image_name = "media/turret_up.png"

        self.image = pygame.transform.scale(pygame.image.load(path + image_name).convert_alpha(),
                                                (tile_size, tile_size))
        if direction == 'right':
            self.image = pygame.transform.flip(self.image, True, False)
        if direction == "down":
            self.image = pygame.transform.flip(self.image,False,True)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.topleft = (pos[0] * tile_size, pos[1] * tile_size)
        self.map = tiles
        self.tile_size = tile_size
        self.laser_range = 0
        for i in range(50):
            if direction == "up":
                tile = self.map[pos[0]][pos[1]+i]
            elif direction == "down":
                tile = self.map[pos[0]][pos[1]-i]
            elif direction == "left":
                tile = self.map[pos[0]-i][pos[1]]
            elif direction == "right":
                tile = self.map[pos[0]+i][pos[1]]
            if tile != "0":
                break
            self.laser_range += 1
        if direction == "up":
            tile = self.map[pos[0]][pos[1] + 1]
        elif direction == "down":
            tile = self.map[pos[0]][pos[1] - 1]
        elif direction == "left":
            tile = self.map[pos[0] - 1][pos[1]]
        elif direction == "right":
            tile = self.map[pos[0] + 1][pos[1]]
        self.laser = Laser(self.path,self.laser_range,tile, tile_size, direction)
        self.laser_image = pygame.transform.scale(pygame.image.load(path + 'media/laser-shot.png').convert_alpha(),
                                                  (tile_size, tile_size))


class Laser(pygame.sprite.Sprite):
    def __init__(self, path, range, pos, tile_size, direction):
        super().__init__()
        self.laser_image = pygame.transform.scale(pygame.image.load(path + 'media/laser-shot.png').convert_alpha(),
                                                  (tile_size, tile_size))
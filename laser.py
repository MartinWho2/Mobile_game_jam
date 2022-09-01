import pygame


class Tower(pygame.sprite.Sprite):
    def __init__(self, path, pos: tuple,num:int, direction,opened, tile_size, tiles):  # Image to be inputted with full path
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

        for i in range(1,50):
            if direction == "up":
                tile = self.map[pos[1]-i][pos[0]]
            elif direction == "down":
                tile = self.map[pos[1]+i][pos[0]]
            elif direction == "left":
                tile = self.map[pos[1]][pos[0]-i]
            elif direction == "right":
                tile = self.map[pos[1]][pos[0]+i]
            if tile != "0":
                break
            self.laser_range += 1
        if direction == "up":
            tile = [pos[0],pos[1] - 1]
        elif direction == "down":
            tile = [pos[0],pos[1] + 1]
        elif direction == "left":
            tile = [pos[0] - 1,pos[1]]
        elif direction == "right":
            tile = [pos[0] + 1,pos[1]]
        self.laser = Laser(self.path,self.laser_range,tile, tile_size, direction, num,opened)
        self.lasers = pygame.sprite.Group(self.laser)


class Laser(pygame.sprite.Sprite):
    def __init__(self, path, laser_range, pos, tile_size, direction, num,opened):
        super().__init__()
        img_len = laser_range * tile_size
        self.tile_size = tile_size
        self.img_len = img_len
        self.opened = opened
        self.num = num
        self.laser_image = pygame.transform.scale(pygame.image.load(path + 'media/laser-shot.png').convert_alpha(),
                                                  (tile_size, tile_size))
        self.tiles = []
        if direction in {"up","down"}:
            self.laser_image = pygame.transform.rotate(self.laser_image,90)
            self.image = pygame.surface.Surface((tile_size,img_len),pygame.SRCALPHA)
            for i in range(laser_range):
                self.image.blit(self.laser_image,(0,i*tile_size))
            self.tiles = [pos[1]-laser_range,pos[1]]
            if direction == "down":
                self.tiles = [pos[1],pos[1]+laser_range]
        else:
            self.image = pygame.surface.Surface((img_len,tile_size),pygame.SRCALPHA)
            for i in range(laser_range):
                self.image.blit(self.laser_image,(i*tile_size,0))
            self.tiles = [pos[0] - laser_range, pos[0]]
            if direction == "right":
                self.tiles = [pos[0], pos[0] + laser_range]

        self.rect = self.image.get_rect()
        if direction == "up":
            self.rect.bottomleft = (pos[0] * tile_size, (pos[1]+1) * tile_size)
        elif direction == "down":
            self.rect.topleft = (pos[0] * tile_size, pos[1] * tile_size)
        elif direction == "left":
            self.rect.topright = ((pos[0]+1) * tile_size, pos[1] * tile_size)
        elif direction == "right":
            self.rect.topleft = (pos[0] * tile_size, pos[1] * tile_size)
        self.mask = pygame.mask.from_surface(self.image)
        self.direction = direction

import pygame
import math

from moving_sprite import Moving_sprite
from laser import Laser


class Arm(Moving_sprite):
    def __init__(self, window, default_spawn: pygame.Vector2, movement: pygame.Vector2, tiles: list, tile_factor: int,
                 groups_colliding, groups_including, player_size: int, path: str, arm_finish: pygame.sprite.Group):
        if movement.x > 0:
            angle = -math.degrees(math.atan(movement.y / movement.x))
        elif movement.x < 0:
            angle = 180 - math.degrees(math.atan(movement.y / movement.x))
        elif movement.x == 0:
            if movement.y < 0:
                angle = 90
            else:
                angle = -90
        image = pygame.transform.rotate(pygame.image.load(path + 'media/arm.png').convert_alpha(), angle + 90)
        super().__init__(default_spawn, image, image.get_width(), tiles, tile_factor, groups_colliding,
                         groups_including, image.get_height())
        self.rect.center = default_spawn.x, default_spawn.y
        self.window = window
        self.movement = movement
        self.movement.scale_to_length(round(self.tile_size / 2))
        self.moving = True
        self.w, self.h = self.window.get_width(), self.window.get_height()
        self.arm_finish = arm_finish

    def move(self, dt, lasers, game):
        self.speed = self.movement * dt
        self.pos += self.speed
        self.rect.x = round(self.pos.x)
        hits = self.check_collision(breaking=True, game=game)
        self.collide(hits, False)
        self.rect.y = round(self.pos.y)
        if hits:
            self.movement = 0, 0
            self.moving = False
            self.arm_finish.add(self)
            self.laser_collide(lasers, game)
            return
        hits = self.check_collision(breaking=True, game=game)
        self.collide(hits, True)
        if hits:
            self.movement = 0, 0
            self.moving = False
            self.arm_finish.add(self)
            self.laser_collide(lasers, game)

    def laser_collide(self, lasers, game):
        laser = self.check_collision(tiles=False, sprite_groups=[lasers], return_sprite=True)
        if laser:
            laser: Laser
            game.rects_to_update.append(laser.rect.copy())
            collision_mask = laser.mask.overlap_mask(self.mask,
                                                     (self.rect.x - laser.rect.x, self.rect.y - laser.rect.y))
            arm_tile = (math.floor(self.rect.centerx / self.tile_size), math.floor(self.rect.centery / self.tile_size))
            print("Arm pos: ", arm_tile, laser.tiles)
            found = self.check_mask_laser(laser.direction, collision_mask)
            if laser.direction in {"up", "down"}:
                laser_image = pygame.surface.Surface((laser.rect.w, found), pygame.SRCALPHA)
                if laser.direction == "up":
                    laser_image.blit(laser.image, (0, -laser.rect.h + found))
                else:
                    laser_image.blit(laser.image, (0, 0))
                laser.image = laser_image
                laser.mask = pygame.mask.from_surface(laser.image)
                if laser.direction == "up":
                    laser.rect = laser.image.get_rect(bottomleft=laser.rect.bottomleft)
                else:
                    laser.rect = laser.image.get_rect(topleft=laser.rect.topleft)

            else:
                print("collided with arm ", laser.direction, "found collision at pixel ", found)
                laser_image = pygame.surface.Surface((found, laser.rect.h), pygame.SRCALPHA)
                if laser.direction == "left":
                    laser_image.blit(laser.image, (-laser.rect.w + found, 0))
                else:
                    laser_image.blit(laser.image, (0, 0))
                laser.image = laser_image
                laser.mask = pygame.mask.from_surface(laser.image)
                if laser.direction == "left":
                    laser.rect = laser.image.get_rect(topright=laser.rect.topright)
                else:
                    laser.rect = laser.image.get_rect(topleft=laser.rect.topleft)

            game.sprites_to_update.append(laser)

    def check_mask_laser(self, direction: str, mask: pygame.mask.Mask):
        size = mask.get_size()
        print("Size of mask ", size)
        found = False
        if direction == "up":
            for row in reversed(range(size[1])):
                for column in range(size[0]):
                    if mask.get_at((column, row)) == 1:
                        found = size[1] - row
                        break
        elif direction == "down":
            for row in range(size[1]):
                for column in range(size[0]):
                    if mask.get_at((column, row)) == 1:
                        found = row
                        break
        elif direction == "left":
            for column in reversed(range(size[0])):
                for row in range(size[1]):
                    if mask.get_at((column, row)) == 1:
                        found = size[0] - column
                        break
        elif direction == "right":
            for column in range(size[0]):
                for row in range(size[1]):
                    if mask.get_at((column, row)) == 1:
                        found = column
                        break
        return found

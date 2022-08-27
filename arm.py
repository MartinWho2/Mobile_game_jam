import pygame
import math
from moving_sprite import Moving_sprite


class Arm(Moving_sprite):
    def __init__(self, window, default_spawn: pygame.Vector2, movement: pygame.Vector2, tiles: list, tile_factor:int, groups_colliding, groups_including, player_size: int, path: str, arm_finish: pygame.sprite.Group):
        if movement.x > 0:
            angle = -math.degrees(math.atan(movement.y/movement.x))
        elif movement.x < 0:
            angle = 180 - math.degrees(math.atan(movement.y/movement.x))
        elif movement.x == 0:
            if movement.y < 0:
                angle = 90
            else:
                angle = -90
        image = pygame.transform.rotate(pygame.image.load(path + 'media/arm.png').convert_alpha(), angle+90)
        super().__init__(default_spawn, image, image.get_width(), tiles, tile_factor, groups_colliding, groups_including, image.get_height())
        self.rect.centerx = default_spawn.x
        if movement.y < 0:
            self.rect.y = default_spawn.y + 25

        self.rect.center = default_spawn.x, default_spawn.y
        self.window = window
        self.movement = movement
        self.movement.scale_to_length(20)
        self.moving = True
        self.w, self.h = self.window.get_width(), self.window.get_height()
        self.arm_finish = arm_finish

    def move(self, dt):
        self.speed = self.movement*dt
        self.pos += self.speed
        self.rect.x = round(self.pos.x)
        hits = self.check_collision(breaking=True)
        self.collide(hits, False)
        self.rect.y = round(self.pos.y)
        if hits:
            self.movement = 0, 0
            self.moving = False
            self.arm_finish.add(self)
        hits = self.check_collision(breaking=True)
        self.collide(hits, True)
        if hits:
            self.movement = 0, 0
            self.moving = False
            self.arm_finish.add(self)




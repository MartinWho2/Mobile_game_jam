import pygame
from moving_sprite import Moving_sprite
from arm import Arm


class Player(Moving_sprite):
    def __init__(self, spawn: pygame.Vector2, map, tile_size: int, window: pygame.Surface, path: str,
                 groups_colliding, player_sprite_group, arm_sprite):
        super().__init__(spawn, pygame.image.load(path + "media/robot_petit_3.png").convert_alpha(), round(tile_size * 2.5), map,
                         tile_size, groups_colliding, player_sprite_group)
        self.window = window
        self.map = map
        self.tile_size = tile_size
        self.groups_colliding = groups_colliding
        self.player_sprite_group = player_sprite_group
        self.w, self.h = self.window.get_width(), self.window.get_height()
        self.state = 'idle'
        self.path = path

        self.glass_group = self.groups_colliding[1]

        # Arms
        self.arms_finish = arm_sprite
        self.arms = pygame.sprite.Group()
        self.idle_mask = pygame.image.load(self.path+"media/player/idle_mask.png").convert_alpha()
        idle_mask = pygame.mask.from_surface(self.idle_mask)
        self.masks = {"idle":idle_mask}

    def move(self, game, dt):
        # Key input
        self.speed.x = 0
        if game.buttons[game.button_left]:
            self.speed.x += -self.w / 350 * dt
        if game.buttons[game.button_right]:
            self.speed.x += self.w / 350 * dt
        self.pos.x += self.speed.x
        self.rect.x = round(self.pos.x)
        hits = self.check_collision()
        if hits:
            movement = self.collide(hits, False)
        self.fall(dt)

        # Update state
        if self.is_jumping:
            self.state = 'jump'
        elif self.speed.x < 0:
            self.state = 'run_left'
        elif self.speed.x > 0:
            self.state = 'run_right'
        else:
            self.state = 'idle'

    def jump(self):
        if not self.is_jumping:
            self.is_jumping = True
            self.speed.y = -7

    def launch_arm(self, movement):
        center = pygame.Vector2(self.rect.centerx, self.rect.centery)
        arm = Arm(self.window, center, movement, self.map, self.tile_size, self.groups_colliding,
                  self.player_sprite_group, 2 * self.tile_size, self.path,self.arms_finish)
        self.arms.add(arm)

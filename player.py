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
        self.idle_mask_mask = pygame.mask.from_surface(self.idle_mask)
        idle_mask = self.idle_mask_mask
        #self.debug_print_mask([self.idle_mask_mask])
        self.mask = idle_mask

    def move(self, game, dt):
        # Key input
        self.speed.x = 0
        if game.buttons[game.button_left] is not False:
            self.speed.x += -self.w / 350 * dt
        if game.buttons[game.button_right] is not False:
            self.speed.x += self.w / 350 * dt
        self.pos.x += self.speed.x
        self.rect.x = round(self.pos.x)
        hits = self.check_collision()
        if hits:
            movement = self.collide(hits, False)
        #if self.check_collision():
            #print("collision again")
            #print(self.mask==self.idle_mask_mask)
            #print(self.debug_print_mask(self.check_collision()))
            #print("class is ",self.check_collision(tiles=False,return_sprite=True).__class__)
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

        self.state += f'_{game.arms_available}'

    def jump(self):
        if not self.is_jumping:
            self.is_jumping = True
            self.speed.y = -8

    def launch_arm(self, movement, launch_place):
        center = pygame.Vector2(self.rect.centerx, self.rect.centery)
        launch = pygame.Vector2((launch_place.x - center.x)/2+center.x,(launch_place.y - center.y)/2+center.y)
        arm = Arm(self.window, launch, movement, self.map, self.tile_size, self.groups_colliding,
                  self.player_sprite_group, 2 * self.tile_size, self.path,self.arms_finish)
        self.arms.add(arm)

    def running_player(self, game, dt):
        self.speed.x += self.w / 350 * dt

        if self.rect.x > self.w:
            self.rect.x = -self.rect.w

    def debug_print_mask(self,masks:list[pygame.mask.Mask]):
        for mask in masks:
            size = mask.get_size()
            for y in range(size[1]):
                for x in range(size[0]):
                    print(mask.get_at((x,y)),end="")
                print("")
            print("END MASK\n\n")
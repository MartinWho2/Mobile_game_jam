import pygame
from moving_sprite import Moving_sprite
from arm import Arm
from fonctions import show_mask


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
        self.hitbox, self.hitbox_diff = self.create_hitbox(idle_mask,self.pos)


    def reput_hitbox(self):
        self.hitbox.topleft = (self.rect.x+self.hitbox_diff[0],self.rect.y+self.hitbox_diff[1])
    def create_hitbox(self,mask,offset):
        size = mask.get_size()
        firstPixel = [0,0]
        for y in range(size[1]):
            exiting = False
            for x in range(size[0]):
                if mask.get_at((x,y)) != 0:
                    firstPixel = [x,y]
                    exiting = True
                    break
            if exiting:
                break


        width = 0
        for x in range(firstPixel[0],size[0]):
            width += 1
            if mask.get_at((x,firstPixel[1])) != 1:
                break
        height = 0
        for y in range(firstPixel[1], size[1]):
            height += 1
            if mask.get_at((firstPixel[0], y)) == 0:
                break
        return pygame.rect.Rect(firstPixel[0]+offset.x,firstPixel[1]+offset.y,width,height),firstPixel

    def move(self, game, dt):
        # Key input
        self.speed.x = 0
        if game.buttons[game.button_left] is not False:
            self.speed.x -= 3 * dt
        if game.buttons[game.button_right] is not False:
            self.speed.x += 3 * dt
        self.pos.x += self.speed.x
        self.rect.x = round(self.pos.x)
        self.reput_hitbox()
        self.pos += self.check_collision_opti(self.speed,False,game)
        self.rect.x = round(self.pos.x)
        #hits = self.check_collision()
        #if hits:
        #    movement = self.collide(hits, False)
        #if self.check_collision():
            #print("collision again")
            #print(self.mask==self.idle_mask_mask)
            #print(self.debug_print_mask(self.check_collision()))
            #print("class is ",self.check_collision(tiles=False,return_sprite=True).__class__)
        self.reput_hitbox()
        #game.window.blit(self.mask.to_surface(), (self.rect.x + game.offset[0], self.rect.y + game.offset[1]))

        self.fall(dt,game)
        #pygame.draw.rect(game.window, "red", (self.hitbox.x + game.offset[0], self.hitbox.y + game.offset[1],
        #                                      self.hitbox.w, self.hitbox.h))
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

    def launch_arm(self, movement):
        center = pygame.Vector2(self.rect.centerx, self.rect.centery)
        arm = Arm(self.window, center, movement, self.map, self.tile_size, self.groups_colliding,
                  self.player_sprite_group, 2 * self.tile_size, self.path,self.arms_finish)
        self.arms.add(arm)

    def running_player(self, game, dt):
        self.speed.x += self.w / 350 * dt

        if self.rect.x > self.w:
            self.rect.x = -self.rect.w


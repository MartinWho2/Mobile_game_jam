import pygame
from moving_sprite import Moving_sprite


class Head(Moving_sprite):
    def __init__(self, player_pos: pygame.Vector2, tiles, tile_size: int, window: pygame.Surface, path: str,
                 groups_colliding, head_sprite_group, player_speed, game):
        self.image = pygame.image.load(path + 'media/head.png').convert_alpha()
        self.path = path
        player_pos.x += tile_size * 5 / 8
        super().__init__(player_pos, self.image, round(tile_size * 5 / 8), tiles, tile_size, groups_colliding,
                         head_sprite_group)
        self.on_ground = False
        self.is_jumping = True
        self.window = window
        self.w, self.h = self.window.get_size()
        self.state = 'jump'
        self.idle_mask = pygame.image.load(self.path + "media/head/idle_mask.png").convert_alpha()
        idle_mask = pygame.mask.from_surface(self.idle_mask)
        self.masks = {"idle": idle_mask}
        self.idle_idle_mask = idle_mask
        self.animate_detachment(player_speed, game)
        self.hitbox = self.mask.get_rect(midbottom=(self.rect.right, self.rect.bottom + self.rect.h))
        self.hitbox.h *= 6/5
        self.hitbox.w *= 23/25
        self.rect.w *= 2
        self.rect.h *= 2

    def animate_detachment(self,speed:pygame.Vector2, game):
        self.speed = pygame.Vector2(speed.x,speed.y-self.tile_size/10)
        self.fall(1, game)

    def reput_hitbox(self):
        self.hitbox.center = (self.rect.centerx - self.rect.w / 50, self.rect.centery + self.rect.h * 13 / 60)

    def move(self, game, dt):
        # Key input
        self.speed.x = 0
        if game.buttons[game.button_left] is not False:
            self.speed.x += -self.w / 230 * dt
        if game.buttons[game.button_right] is not False:
            self.speed.x += self.w / 230 * dt
        self.pos.x += self.speed.x
        self.rect.x = round(self.pos.x)
        self.reput_hitbox()
        #hits = self.check_collision()
        #if hits:
        #    self.collide(hits, False)  # Horizontal hits
        self.pos += self.check_collision_opti(self.speed,False,game)
        self.rect.x = round(self.pos.x)
        self.reput_hitbox()
        self.fall(dt, game)  # Vertical hits, see moving_sprite.py


        print(self.rect.w)
        #pygame.draw.rect(game.window, "red",
        #                 (self.rect.x + game.offset[0], self.rect.y + game.offset[1],
        #                  self.rect.w, self.rect.h))
        #pygame.draw.rect(game.window,"black",(self.hitbox.x+game.offset[0],self.hitbox.y+game.offset[1],
        #                                      self.hitbox.w,self.hitbox.h))
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
        if self.on_ground:
            self.state = 'jump'
            self.is_jumping = True
            self.on_ground = False
            self.speed.y = -6

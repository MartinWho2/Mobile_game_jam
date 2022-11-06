import pygame
from moving_sprite import Moving_sprite


class Head(Moving_sprite):
    def __init__(self, player_pos: pygame.Vector2, tiles, tile_size: int, window: pygame.Surface, path: str,
                 groups_colliding, head_sprite_group):
        self.image = pygame.image.load(path + 'media/head.png').convert_alpha()
        self.path = path
        super().__init__(player_pos, self.image, round(tile_size * 5 / 8), tiles, tile_size, groups_colliding,
                         head_sprite_group)
        self.window = window
        self.w, self.h = self.window.get_size()
        self.state = 'jump'
        self.idle_mask = pygame.image.load(self.path + "media/head/idle_mask.png").convert_alpha()
        idle_mask = pygame.mask.from_surface(self.idle_mask)
        self.masks = {"idle": idle_mask}
        self.idle_idle_mask = idle_mask
        self.animate_detachment()
        self.rect_collision = self.mask.get_rect(midbottom=(self.rect.right,self.rect.bottom+self.rect.h))

    def animate_detachment(self):
        self.speed = pygame.Vector2(-self.w / 200, self.w / 200)

    def move(self, game, dt):
        # Key input
        self.speed.x = 0
        if game.buttons[game.button_left] is not False:
            self.speed.x += -self.w / 230 * dt
        if game.buttons[game.button_right] is not False:
            self.speed.x += self.w / 230 * dt
        self.pos.x += self.speed.x
        self.rect.x = round(self.pos.x)

        hits = self.check_collision()
        if hits:
            self.collide(hits, False)  # Horizontal hits
        self.fall(dt)  # Vertical hits, see moving_sprite.py
        self.rect.y = round(self.pos.y)

        self.rect_collision.midbottom = (self.rect.right,self.rect.bottom+self.rect.h)
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

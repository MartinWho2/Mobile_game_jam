import pygame
from moving_sprite import Moving_sprite


class Head(Moving_sprite):
    def __init__(self, player_pos: pygame.Vector2, tiles, tile_size: int, window: pygame.Surface, path: str,
                 groups_colliding, head_sprite_group):
        self.image = pygame.image.load(path + 'media/head.png').convert_alpha()
        super().__init__(player_pos, self.image, round(tile_size * 5 / 8), tiles, tile_size, groups_colliding,
                         head_sprite_group)
        self.window = window
        self.w, self.h = self.window.get_size()
        self.detached = False
        self.state = None

        self.animate_detachment()

    def animate_detachment(self):
        self.speed = pygame.Vector2(self.w / 200, self.w / 200)

    def move(self, game, dt):
        # Key input
        self.speed.x = 0
        if game.buttons[game.button_left]:
            self.speed.x += -self.w / 230 * dt
        if game.buttons[game.button_right]:
            self.speed.x += self.w / 230 * dt
        self.pos.x += self.speed.x
        self.rect.x = round(self.pos.x)

        hits = self.check_collision()
        if hits:
            self.collide(hits, False)  # Horizontal hits

        self.fall(dt)  # Vertical hits, see moving_sprite.py
        self.rect.y = round(self.pos.y)

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
            self.state = 'jump'
            self.is_jumping = True
            self.speed.y = -5.5

import pygame


class Player():
    def __init__(self, window: pygame.Surface, spawn: pygame.Vector2, tile_size):
        self.window = window
        self.w, self.h = self.window.get_width(), self.window.get_height()
        self.image = None
        self.player_w, self.player_h = 2 * tile_size, 2 * tile_size
        self.rect = pygame.rect.Rect(spawn.x, spawn.y, self.player_w, self.player_h)
        self.position = pygame.Vector2(self.rect.x, self.rect.y)
        self.speed = pygame.Vector2(0, 0)
        self.jumping = None
        self.state = 'idle'  # Possible states: idle, run, jump, climb

    def blit_player(self, scroll: pygame.Vector2, spritesheet, dt):
        self.image = spritesheet.animate(self.state, dt)
        self.window.blit(self.image, (self.rect.x - scroll.x - self.rect.w / 2, self.rect.y - scroll.y - self.rect.h))

    def check_collisions(self, neighbour_tiles, tile_types):
        hit_list = []
        for idx, tile in enumerate(neighbour_tiles):
            if self.rect.colliderect(tile):
                hit_list.append([tile, tile_types[idx]])
        return hit_list

    def move(self, dt, keys):
        # Key input
        jumping_attempt = False
        if keys.get(pygame.K_a):
            self.speed.x = -self.w / 300 * dt
            self.state = 'run_left'
        elif keys.get(pygame.K_d):
            self.speed.x = self.w / 300 * dt
            self.state = 'run_right'
        else:
            self.speed.x = 0
            self.state = 'idle'
        if keys.get(pygame.K_w):
            jumping_attempt = True
            if not self.jumping:
                self.jumping = True
                self.state = 'jump'
                self.speed.y = - self.h / 70 * dt
        if self.speed.y < self.h / 100:
            self.speed.y += 0.7 * dt  # Gravity

        self.rect += self.speed
        self.rect.x = round(self.rect.x)
        self.rect.y = round(self.rect.y)

import pygame
import math

from spritesheet import Spritesheet
from interface_button import Interface_button as Int_button
from fonctions import create_map
from player import Player
from head import Head
from level_infos import dictionnaire


class Game():
    def __init__(self, window: pygame.surface.Surface, path: str):
        self.window = window
        self.path = path
        self.tile_size = 40
        self.w, self.h = self.window.get_size()
        arrow_right = pygame.image.load(path + "media/arrow.png").convert_alpha()
        arrow_up = pygame.image.load(path + "media/arrow_up.png")
        button = pygame.surface.Surface(arrow_right.get_size())
        button.fill((255, 255, 255))
        pygame.draw.rect(button, (128, 128, 128), arrow_right.get_rect(), width=1)
        jump_button = button.copy()
        jump_button.blit(arrow_up, (0, 0))
        button.blit(arrow_right, (0, 0))
        arrow_left = pygame.transform.flip(button, True, False)
        self.button_right = Int_button(button, pygame.Vector2(self.w / 5, self.h * 6 / 7), round(self.w / 8),
                                       name="right")
        self.button_left = Int_button(arrow_left, pygame.Vector2(self.w / 40, self.h * 6 / 7), round(self.w / 8),
                                      name="left")
        self.button_up = Int_button(jump_button, pygame.Vector2(self.w * 6 / 7, self.h * 6 / 7), round(self.w / 8),
                                    name="up")
        square_button = pygame.transform.scale(pygame.image.load(path + 'media/squared_button.png').convert_alpha(),
                                               (100, 100))
        pause_button = square_button.copy()
        pause_image = pygame.transform.scale(pygame.image.load(path + 'media/pause.png').convert_alpha(), (100, 100))
        pause_button.blit(pause_image, (0, 0))
        self.pause_button = Int_button(pause_button, pygame.Vector2(self.w - 105, 5), 100, name="pause")
        reset_button = square_button.copy()
        reset_image = pygame.transform.scale(pygame.image.load(path + 'media/reset.png').convert_alpha(), (100, 100))
        reset_button.blit(reset_image, (0, 0))
        self.reset_button = Int_button(reset_button, pygame.Vector2(self.w - 210, 5), 100, name="reset")
        action_surface = pygame.Surface((round(self.w / 8), round(self.w / 8)))
        pygame.draw.circle(action_surface, (150, 150, 150), (round(self.w / 16), round(self.w / 16)),
                           round(self.w / 16))
        self.action_button = Int_button(action_surface, pygame.Vector2(self.w * 5 / 7, self.h * 6 / 7),
                                        round(self.w / 16), name="action")
        self.level = 1
        self.buttons_interface = pygame.sprite.Group(self.button_right, self.button_left, self.button_up,
                                                     self.pause_button, self.reset_button, self.action_button)
        self.buttons = {self.button_left: False, self.button_right: False, self.button_up: False,
                        self.pause_button: False, self.action_button: False}
        self.map = create_map(self.path, self.level)
        self.tile_image = pygame.transform.scale(pygame.image.load(self.path + "media/tile_test.png").convert_alpha(),(self.tile_size, self.tile_size))
        self.glass_image = pygame.transform.scale(pygame.image.load(self.path + 'media/vitre.png').convert_alpha(),(self.tile_size, self.tile_size))
        self.vent_image = pygame.transform.scale(pygame.image.load(self.path + 'media/vent.png').convert_alpha(),(self.tile_size, self.tile_size))
        self.back_tile_image = pygame.transform.scale(pygame.image.load(self.path + "media/back_tile.png").convert_alpha(),(self.tile_size, self.tile_size))

        # Sprites
        self.player_sprite = pygame.sprite.Group()
        self.laser_sprites = pygame.sprite.Group()
        self.head_sprite = pygame.sprite.Group()
        self.arm_sprite = pygame.sprite.Group()
        self.buttons_in_game = pygame.sprite.Group()
        self.door_sprites = pygame.sprite.Group()
        self.glass_sprites = pygame.sprite.Group()
        self.collidable_sprites = [self.door_sprites, self.glass_sprites,self.arm_sprite]

        # Player
        self.player = Player(pygame.Vector2(0, 100), self.map, self.tile_size, self.window, self.path,
                             self.collidable_sprites,[self.player_sprite],self.arm_sprite)
        self.head = Head(pygame.Vector2(0, 0), self.map, self.tile_size, self.window, self.path,
                         self.collidable_sprites, [self.head_sprite])
        self.player_or_head = True  # Player is True, head is False
        self.arm_detached = False

        # Arms
        self.arms_available = 10
        self.arms_direction = pygame.Vector2(0, 0)
        self.pointing_arrow = pygame.image.load(path + "media/pointing_arrow.png").convert_alpha()
        self.distance = 0

        # Images
        self.player_spritesheet = Spritesheet('player', path)
        self.head_spritesheet = Spritesheet('head', path)

        self.levels_infos = dictionnaire


    def update(self, dt):
        self.blit_map()
        for button in self.buttons_interface:
            self.window.blit(button.image, button.rect)

        if self.player_or_head:
            self.player.move(self, dt)
        else:
            self.player.fall(dt)
            self.head.move(self, dt)
            self.blit_head(self.head_spritesheet, dt)

        self.blit_player(self.player_spritesheet, dt)
        # Arms
        if self.action_button.clicking:
            pos = pygame.mouse.get_pos()
            self.distance = pygame.Vector2(pos[0], pos[1]).distance_to(self.action_button.rect.center)
            if self.distance > self.action_button.rect.w/2:
                self.arm_aiming(self.action_button.rect.center, pos)
        self.player.arms.draw(self.window)
        for arm in self.player.arms:
            if arm.moving:
                arm.move(dt)

    def load_new_level(self, level: int):
        self.level = level
        self.map = create_map(self.path, level)

    def blit_map(self):
        for row in range(len(self.map)):
            for column in range(len(self.map[row])):
                tile = self.map[row][column]
                #if tile == "0":
                #    self.window.blit(self.back_tile_image,(column * self.tile_size, row * self.tile_size))
                if tile == "1":
                    self.window.blit(self.tile_image, (column * self.tile_size, row * self.tile_size))
                if tile == "2":
                    self.window.blit(self.glass_image, (column * self.tile_size, row * self.tile_size))

    def blit_player(self, spritesheet, dt):
        self.player.image = spritesheet.animate(self.player.state, dt)
        # self.player.mask = pygame.mask.from_surface(self.player.image)
        self.player.mask = self.player.masks["idle"]
        # self.window.blit(self.player.idle_mask,self.player.rect)
        self.window.blit(self.player.image, (self.player.rect.x, self.player.rect.y))

    def blit_head(self, spritesheet, dt):
        self.head.image = spritesheet.animate(self.head.state, dt)
        self.head.mask = pygame.mask.from_surface(self.head.image)
        self.window.blit(self.head.image, (self.head.rect.x, self.head.rect.y))

    def arm_aiming(self, initial_pos, actual_pos):
        if self.arms_available > 0:
            dx = actual_pos[0] - initial_pos[0]
            dy = actual_pos[1] - initial_pos[1]
            if dx == 0:
                angle = 90
            elif dx < 0:
                angle = 180 - math.degrees(math.atan(dy / dx))
            else:
                angle = -math.degrees(math.atan(dy / dx))
            pointing_arrow = pygame.transform.rotate(self.pointing_arrow, angle)
            rect1 = pointing_arrow.get_rect()
            rect2 = pointing_arrow.get_rect()
            center = pygame.Vector2(dx, dy)
            if center.length() != 0:
                center.scale_to_length(self.w / 16)
            rect1.center = initial_pos + center
            rect2.center = self.player.rect.center + center
            self.window.blit(pointing_arrow, rect1)
            self.window.blit(pointing_arrow, rect2)
            self.arms_direction = center

    def restart(self):
        self.load_new_level(self.level)
        self.player = Player(pygame.Vector2(0, 100), self.map, self.tile_size, self.window, self.path,
                             self.collidable_sprites, [self.player_sprite], self.arm_sprite)



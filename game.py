import pygame
import math

from spritesheet import Spritesheet
from interface_button import Interface_button as Int_button
from fonctions import create_map
from player import Player
from head import Head
from level_infos import dictionnaire
from vent import Vent
from door import Door
from button import Button
from laser import Tower
from portal import Portal
from text import Text


class Game():
    def __init__(self, window: pygame.surface.Surface, path: str):
        self.window = window
        self.menu_music = pygame.mixer.Sound(path+"media/menu_music.wav")
        self.level_music = pygame.mixer.Sound(path+"media/level_music.wav")
        self.music = pygame.mixer.Channel(1)
        self.music.set_volume(0.5)
        self.music.play(self.menu_music,-1)
        self.path = path
        self.tile_size = 40
        self.w, self.h = self.window.get_size()
        print(self.w,self.h)
        self.offset = ((self.w-30*self.tile_size)/2,50)
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
        action_surface = pygame.image.load(self.path + 'media/action_button.png').convert_alpha()
        self.action_button = Int_button(action_surface, pygame.Vector2(self.w * 5 / 7, self.h * 5.5 / 7),
                                        round(self.w / 16), name="action")
        action2_surface = pygame.image.load(self.path + 'media/action_button.png').convert_alpha()
        self.action2_button = Int_button(action2_surface, pygame.Vector2(self.w * 4 / 7, self.h * 5.5 / 7),
                                        round(self.w / 16), name="action2")
        self.level = 1
        self.buttons_interface = pygame.sprite.Group(self.button_right, self.button_left, self.button_up,
                                                     self.pause_button, self.reset_button, self.action_button, self.action2_button)
        self.buttons = {self.button_left: False, self.button_right: False, self.button_up: False,
                        self.pause_button: False, self.action_button: False, self.action2_button: False}
        self.map = create_map(self.path, self.level)

        self.tile_image = pygame.transform.scale(pygame.image.load(self.path + "media/tile_test.png").convert_alpha(),
                                                 (self.tile_size, self.tile_size))
        self.glass_image = pygame.transform.scale(pygame.image.load(self.path + 'media/vitre.png').convert_alpha(),
                                                  (self.tile_size, self.tile_size))
        self.vent_image = pygame.transform.scale(pygame.image.load(self.path + 'media/vent.png').convert_alpha(),
                                                 (self.tile_size, self.tile_size))
        self.back_tile_image = pygame.transform.scale(
            pygame.image.load(self.path + "media/back_tile.png").convert_alpha(), (self.tile_size, self.tile_size))
        self.map_image = self.create_map_image()
        # Sprites
        self.player_sprite = pygame.sprite.Group()
        self.laser_sprites = pygame.sprite.Group()
        self.opened_laser_sprites = pygame.sprite.Group()
        self.head_sprite = pygame.sprite.Group()
        self.arm_sprite = pygame.sprite.Group()
        self.buttons_in_game = pygame.sprite.Group()
        self.door_sprites = pygame.sprite.Group()
        self.opened_door_sprites = pygame.sprite.Group()
        self.glass_sprites = pygame.sprite.Group()
        self.vent_sprites = pygame.sprite.Group()
        self.tower_sprites = pygame.sprite.Group()
        self.laser_sprites = pygame.sprite.Group()
        self.portal_sprites = pygame.sprite.Group()
        self.collidable_sprites = [self.door_sprites, self.glass_sprites, self.arm_sprite, self.tower_sprites]
        self.texts = []

        # Player
        self.player = Player(pygame.Vector2(0, 100), self.map, self.tile_size, self.window, self.path,
                             self.collidable_sprites, [self.player_sprite], self.arm_sprite, )
        self.head = Head(pygame.Vector2(0, 0), self.map, self.tile_size, self.window, self.path,
                         self.collidable_sprites, [self.head_sprite])
        self.player_or_head = True  # Player is True, head is False
        self.arm_detached = False

        # Arms
        self.arms_available = 2
        self.arms_direction = pygame.Vector2(0, 0)
        self.pointing_arrow = pygame.image.load(path + "media/pointing_arrow.png").convert_alpha()
        self.distance = 0

        # Images
        self.player_spritesheet = Spritesheet('player', path)
        self.head_spritesheet = Spritesheet('head', path)

        self.levels_infos = dictionnaire
        self.portal_rect = pygame.rect.Rect(0, 0, 10, 10)  # Modifié dans load level

    def update(self, dt):
        print(f"dt = {dt}")
        time = pygame.time.get_ticks()
        self.blit_map()
        for text in self.texts:
            self.window.blit(text.image, (text.rect.x+self.offset[0],text.rect.y+self.offset[1]))
        time2 = pygame.time.get_ticks()
        print(f"The map is blitted in {time2-time} ms")
        for button in self.buttons_interface:
            self.window.blit(button.image, (button.rect.x, button.rect.y))
        time = pygame.time.get_ticks()
        print(f"The buttons are blitted in {time - time2} ms")
        if self.player_or_head:
            self.player.move(self, dt)
            time2 = pygame.time.get_ticks()
            print(f"The player movements are done in {time2 - time} ms")
        else:
            self.player.fall(dt)
            time2 = pygame.time.get_ticks()
            print(f"The player falling is done in {time2 - time} ms")
            self.head.move(self, dt)
            time = pygame.time.get_ticks()
            print(f"The head moves in {time - time2} ms")
            self.blit_head(self.head_spritesheet, dt)
            time2 = pygame.time.get_ticks()
            print(f"The head moves in {time2 - time} ms")

        self.blit_player(self.player_spritesheet, dt)
        time = pygame.time.get_ticks()
        print(f"The player is blitted in {time - time2} ms")
        # Action button
        if self.action_button.clicking:
            if self.player_or_head:
                pos = pygame.mouse.get_pos()
                self.distance = pygame.Vector2(pos[0], pos[1]).distance_to(self.action_button.rect.center)
                if self.distance > self.action_button.rect.w / 2:
                    self.arm_aiming(self.action_button.rect.center, pos)

        time = pygame.time.get_ticks()
        for arm in self.player.arms:
            self.window.blit(arm.image,(arm.rect.x+self.offset[0],arm.rect.y+self.offset[1]))
        time2 = pygame.time.get_ticks()
        print(f"The arms are blitted in {time2 - time} ms")
        for arm in self.player.arms:
            if arm.moving:
                arm.move(dt,self.laser_sprites)
        print(f"the arms move in {pygame.time.get_ticks()-time2} ms")

        # Check if game is over
        if self.head.rect.colliderect(self.portal_rect) or self.player.rect.colliderect(self.portal_rect):
            self.level += 1
            if self.level <= 8:
                self.restart()
            else:
                return 'end'

        if not self.player_or_head:
            if self.head.check_collision(tiles=False,sprite_groups=[self.laser_sprites]):
                self.restart()
        if self.player.check_collision(tiles=False,sprite_groups=[self.laser_sprites]):
            self.restart()

        if 31*self.tile_size < self.player.pos.x < 0 or 16*self.tile_size < self.player.pos.y < 0:
            self.restart()
    def load_new_level(self):
        self.texts = []
        self.door_sprites.empty()
        self.opened_door_sprites.empty()
        self.portal_sprites.empty()
        self.buttons_in_game.empty()
        self.vent_sprites.empty()
        self.laser_sprites.empty()
        self.opened_laser_sprites.empty()
        self.tower_sprites.empty()
        self.player.arms.empty()
        self.arm_sprite.empty()
        self.map = create_map(self.path, self.level)
        self.map_image = self.create_map_image()
        for infos in self.levels_infos['vent'][self.level - 1]:
            vent = Vent(self.path, infos[0], infos[1], infos[2],self.tile_size)
            vent2 = Vent(self.path, infos[1], infos[0], infos[2],self.tile_size)
            self.vent_sprites.add(vent)
            self.vent_sprites.add(vent2)
        for infos in self.levels_infos['door'][self.level - 1]:
            door = Door(self.path, infos[0], infos[1], self.tile_size, infos[2], infos[3])
            if door.opened:
                self.opened_door_sprites.add(door)
            else:
                self.door_sprites.add(door)
        for infos in self.levels_infos['button'][self.level - 1]:
            button = Button(self.path, infos[0], infos[1], self.tile_size)
            self.buttons_in_game.add(button)
        for infos in self.levels_infos['laser'][self.level - 1]:
            laser = Tower(self.path, infos[0], infos[1],infos[2], infos[3], self.tile_size,self.map)
            self.tower_sprites.add(laser)
            if laser.laser.opened:
                self.opened_laser_sprites.add(laser.laser)
            else:
                self.laser_sprites.add(laser.laser)
        for infos in self.levels_infos['portal'][self.level - 1]:
            portal = Portal(self.path, infos, self.tile_size)
            if portal.type == 'end':
                self.portal_rect = portal.rect
            self.portal_sprites.add(portal)
        for infos in self.levels_infos['texts'][self.level-1]:
            text = Text(infos[0], infos[1], self.tile_size)
            self.texts.append(text)


    def blit_map(self):
        timing = pygame.time.get_ticks()
        self.window.blit(self.map_image, (self.offset[0], self.offset[1]))
        timing_2 = pygame.time.get_ticks()
        #print(f"blit map {timing_2-timing} ms")
        for r_index, row in enumerate(self.map):
            for c_index, item in enumerate(row):
                tile = item
                if tile == 2:
                    self.window.blit(self.glass_image, (c_index * self.tile_size+self.offset[0], r_index * self.tile_size+self.offset[1]))
        timing = pygame.time.get_ticks()
        #print(f"blit glass {timing - timing_2}")
        for vent in self.vent_sprites:
            self.window.blit(vent.image,(vent.rect.x+self.offset[0],vent.rect.y+self.offset[1]))
        timing_2 = pygame.time.get_ticks()
        for button in self.buttons_in_game:
            if button.on == True:
                self.window.blit(button.image_on, (button.rect.x+self.offset[0],button.rect.y+self.offset[1]))
            else:
                self.window.blit(button.image_off, (button.rect.x+self.offset[0],button.rect.y+self.offset[1]))
        #print(f"blit vent {timing_2 - timing} ms")
        for door in self.door_sprites:
            self.window.blit(door.image,(door.rect.x+self.offset[0],door.rect.y+self.offset[1]))
        timing = pygame.time.get_ticks()
        #print(f"blit doors {timing - timing_2}")
        for laser in self.laser_sprites:
            self.window.blit(laser.image,(laser.rect.x+self.offset[0],laser.rect.y+self.offset[1]))
        for tower in self.tower_sprites:
            self.window.blit(tower.image,(tower.rect.x+self.offset[0],tower.rect.y+self.offset[1]))
        for portal in self.portal_sprites:
            self.window.blit(portal.image, (portal.rect.x+self.offset[0],portal.rect.y+self.offset[1]))

    def create_map_image(self):
        map_y, map_x = len(self.map), len(self.map[1])
        map_image = pygame.surface.Surface((map_x * self.tile_size, map_y * self.tile_size))
        for r_index, row in enumerate(self.map):
            for c_index, item in enumerate(row):
                tile = item
                if tile != 1:
                    pygame.draw.rect(map_image,(255,255,255),pygame.rect.Rect(c_index * self.tile_size, r_index * self.tile_size,self.tile_size,self.tile_size))
                    #map_image.blit(self.back_tile_image, (c_index * self.tile_size, r_index * self.tile_size))
                if tile == 1:
                    map_image.blit(self.tile_image, (c_index * self.tile_size, r_index * self.tile_size))
        return map_image

    def blit_player(self, spritesheet, dt):
        self.player.image = spritesheet.animate(self.player.state, dt)
        # self.player.mask = pygame.mask.from_surface(self.player.image)
        #self.window.blit(self.player.idle_mask,self.player.rect)
        self.window.blit(self.player.image, (self.player.rect.x+self.offset[0], self.player.rect.y+self.offset[1]))

    def blit_head(self, spritesheet, dt):
        self.head.image = spritesheet.animate(self.head.state, dt)
        #self.player.state = 'without_head'
        #self.head.mask = pygame.mask.from_surface(self.head.image)
        self.head.mask = self.head.masks["idle"]
        #self.window.blit(self.head.idle_mask,(self.head.rect.x, self.head.rect.y))
        #pygame.draw.rect(self.window,(0,0,0),self.head.rect_collision)
        self.window.blit(self.head.image, (self.head.rect.x+self.offset[0], self.head.rect.y+self.offset[1]))

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
            rect2.center = self.player.rect.center + center + self.offset
            self.window.blit(pointing_arrow, rect1)
            self.window.blit(pointing_arrow, rect2)
            self.arms_direction = center

    def restart(self):
        self.load_new_level()
        self.arms_available = 2
        spawn = pygame.Vector2(dictionnaire["spawn"][self.level-1][0],dictionnaire["spawn"][self.level-1][1])
        self.player = Player(spawn, self.map, self.tile_size, self.window, self.path,
                             self.collidable_sprites, [self.player_sprite], self.arm_sprite)
        self.player_or_head = True


import pygame
import player
from fonctions import smallest_rect


class Moving_sprite(pygame.sprite.Sprite):
    def __init__(self, pos: pygame.Vector2, image: pygame.Surface, resize: int, tiles: list, tile_factor: int,
                 groups_colliding: list[pygame.sprite.Group], groups_including: list[pygame.sprite.Group],
                 rectangle=False) -> None:
        super().__init__()
        for sprite_group in groups_including:
            self.add(sprite_group)
        self.sprite_elements = groups_colliding
        self.tiles = tiles
        self.tile_size = tile_factor
        self.pos = pos
        if not rectangle:
            self.image = pygame.transform.scale(image, (resize, resize))
        else:
            self.image = pygame.transform.scale(image, (resize, rectangle))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos.x, pos.y
        self.speed = pygame.Vector2(0, 0)
        self.gravity = self.tile_size / 128
        self.friction = - self.gravity * 1.56
        self.MAX_SPEED = 30 * self.gravity
        self.is_jumping = False
        self.on_ground = True
        self.max_speed = 10
        self.mask = pygame.mask.from_surface(self.image)
        self.flip_mask = 0
        self.tile = pygame.mask.Mask((self.tile_size, self.tile_size), fill=True)
        self.on_platform = False
        self.was_on_platform = 0
        self.map_size = [len(self.tiles), len(self.tiles[0])]
        self.state = None
        self.hitbox = pygame.rect.Rect(0, 0, 0, 0)

    def collide_with_mask(self, mask, pos_mask):
        return self.mask.overlap_mask(mask, (pos_mask[0] - self.rect.x, pos_mask[1] - self.rect.y))

    def check_collision(self, tiles=True, sprite_groups: [str, list] = "normal",
                        return_sprite=False, breaking=False, game=None) -> list[pygame.mask.Mask]:
        if sprite_groups == "normal":
            sprite_groups = self.sprite_elements
        get_hits = []
        if abs(self.speed.y) > 4:
            self.on_ground = False
        # Collision with tiles
        if tiles:
            # Checks for collisions with tiles near the sprite
            a = pygame.time.get_ticks()
            for r_index, row in enumerate(self.tiles):
                for c_index, item in enumerate(row):
                    tile = item
                    if tile != 0 and self.rect.colliderect((c_index * self.tile_size, r_index * self.tile_size,
                                                            self.tile_size, self.tile_size)):
                        mask = self.collide_with_mask(self.tile, (c_index * self.tile_size, r_index * self.tile_size))
                        if mask.count():
                            if item == 2 and breaking:
                                self.tiles[r_index][c_index] = 0
                                rect = pygame.rect.Rect(c_index * self.tile_size, r_index * self.tile_size,
                                                        self.tile_size, self.tile_size)
                                game.rects_to_update.append(self.breaking_glass(r_index, c_index, rect))
                            else:
                                get_hits.append(mask)
            print(f"Collision with : map player {pygame.time.get_ticks() - a}")
        a = pygame.time.get_ticks()
        # Collision with elements
        for group in sprite_groups:
            for element in group:
                if self.rect.colliderect(element.rect):
                    mask = self.collide_with_mask(element.mask, (element.rect.x, element.rect.y))
                    if mask.count():
                        if return_sprite:
                            return element
                        get_hits.append(mask)
        print(f"Collision with sprites : player {pygame.time.get_ticks() - a}")
        return get_hits

    def reput_hitbox(self):
        pass

    def check_collision_opti(self, speed: pygame.Vector2, axis, game, tiles=True, sprite_groups=None,
                             return_sprite=False, breaking=False):
        """
        Real check collision
        :param speed: speed of moving sprite
        :param axis: True for y and False for x
        :param tiles: Do tiles need to be checked
        :param sprite_groups: Sprites to test
        :param return_sprite: Returns a sprite ?
        :param breaking: break the glass ?
        :param masking: Collision with masking
        :param game: Class game
        :return:
        """
        if sprite_groups is None:
            sprite_groups = self.sprite_elements
        need_to_move = pygame.Vector2(0, 0)
        if abs(self.speed.y) > 4:
            self.on_ground = False
        if tiles:
            for r_index, row in enumerate(self.tiles):
                for c_index, tile in enumerate(row):
                    if tile != 0:
                        tile_rect = pygame.rect.Rect(c_index * self.tile_size, r_index * self.tile_size,
                                                     self.tile_size, self.tile_size)
                        if self.hitbox.colliderect(tile_rect):
                            need_to_move = self.collide_opti(need_to_move, axis, speed, tile_rect)
        for group in sprite_groups:
            for element in group:
                if self.hitbox.colliderect(element.rect):
                    if group == game.arm_sprite:
                        mask = self.collide_with_mask(element.mask, (element.rect.x, element.rect.y))
                        if mask.count() and self not in game.player.arms:
                            move = self.collide([mask], axis, move_bool=False)
                            if axis and abs(move) > abs(need_to_move.y):
                                need_to_move.y = move
                            elif (not axis) and abs(move) > abs(need_to_move.x):
                                need_to_move.x = move
                    else:
                        need_to_move = self.collide_opti(need_to_move, axis, speed, element.rect)
                    if return_sprite:
                        return element
        return need_to_move

    def collide_opti(self, need_to_move: pygame.Vector2, axis: bool, speed: pygame.Vector2,
                     tile_rect: pygame.rect.Rect):
        if axis:
            if speed.y > 0:
                move = tile_rect.y - self.hitbox.bottom
                if need_to_move.y > 0:
                    raise Exception
                elif need_to_move.y > move:
                    need_to_move.y = move
                self.on_ground = True
                self.is_jumping = False
                if self.__class__ == player.Player:
                    if 'without_head' not in self.state:
                        self.state = 'idle'
            elif speed.y < 0:
                move = tile_rect.bottom - self.hitbox.y
                if need_to_move.y < 0:
                    raise Exception
                elif need_to_move.y < move:
                    need_to_move.y = move
            speed.y = 0
        else:
            if speed.x > 0:
                move = tile_rect.x - self.hitbox.right
                if need_to_move.x > 0:
                    return "error"
                elif need_to_move.x > move:
                    need_to_move.x = move
            elif speed.x < 0:
                move = tile_rect.right - self.hitbox.x
                if need_to_move.x < 0:
                    return "error"
                elif need_to_move.x < move:
                    need_to_move.x = move
            speed.x = 0
        return need_to_move

    def collide(self, hits: list, axis: bool, move_bool=True) -> int:
        """
        Deals with detected collision
        :param hits: Masks colliding with the entity
        :param axis: True for y and False for x
        :return : movement done after correction
        """
        for mask in hits:
            if axis:
                if self.speed.y > 0:
                    movement = self.find_bits_from_mask(mask, "down")
                    if move_bool:
                        self.pos.y -= movement
                    self.is_jumping = False
                    self.on_ground = True
                    if self.__class__ == player.Player:
                        if 'without_head' not in self.state:
                            self.state = 'idle'
                elif self.speed.y <= 0:
                    movement = self.find_bits_from_mask(mask, "up")
                    if move_bool:
                        self.pos.y += movement
                self.speed.y = 0
                self.rect.y = round(self.pos.y)

            else:
                if self.speed.x > 0:
                    movement = self.find_bits_from_mask(mask, "right")
                    if move_bool:
                        self.pos.x -= movement
                    movement = -movement
                elif self.speed.x <= 0:
                    movement = self.find_bits_from_mask(mask, "left")
                    if move_bool:
                        self.pos.x += movement
                self.speed.x = 0
                self.rect.x = round(self.pos.x)
            return movement

    @staticmethod
    def find_bits_from_mask(mask: pygame.mask.Mask, direction: str) -> int:
        size = mask.get_size()
        found = False
        if direction in {"left", "right"}:
            for column in range(size[0]):
                continue_finding = False
                for row in range(size[1]):
                    coordinate = (column, row)
                    if direction == "left":
                        coordinate = (size[0] - 1 - column, row)
                    if mask.get_at(coordinate) == 1:
                        if not found:
                            found = column
                        continue_finding = True
                if found and not continue_finding:
                    return column - found
            return size[0] - found
        else:
            for row in range(size[1]):
                continue_finding = False
                for column in range(size[0]):
                    coordinate = (column, row)
                    if direction == "up":
                        coordinate = (column, size[1] - 1 - row)
                    if mask.get_at(coordinate) == 1:
                        if not found:
                            found = row
                        continue_finding = True
                        break
                if found and not continue_finding:
                    return row - found
            return size[1] - found

    def fall(self, dt, game):
        self.pos.y += 0.5 * self.gravity * (dt ** 2) + self.speed.y * dt
        self.speed.y += self.gravity * dt
        if self.speed.y > self.MAX_SPEED:
            self.speed.y = self.MAX_SPEED
        self.rect.y = round(self.pos.y)
        self.reput_hitbox()
        self.pos += self.check_collision_opti(self.speed, True, game)
        self.rect.y = round(self.pos.y)
        self.reput_hitbox()

    def breaking_glass(self, row, column, rect: pygame.rect.Rect):
        if self.tiles[row + 1][column] == 2:
            self.tiles[row + 1][column] = 0
            rect = smallest_rect(rect, pygame.rect.Rect(column * self.tile_size, (row+1) * self.tile_size, self.tile_size,
                                                        self.tile_size))
            rect = self.breaking_glass(row + 1, column, rect)
        if self.tiles[row][column + 1] == 2:
            self.tiles[row][column + 1] = 0
            rect = smallest_rect(rect, pygame.rect.Rect((column+1) * self.tile_size, row * self.tile_size, self.tile_size,
                                                        self.tile_size))
            rect = self.breaking_glass(row, column + 1, rect)
        if self.tiles[row - 1][column] == 2:
            self.tiles[row - 1][column] = 0
            rect = smallest_rect(rect, pygame.rect.Rect(column * self.tile_size, (row-1) * self.tile_size, self.tile_size,
                                                        self.tile_size))
            rect = self.breaking_glass(row - 1, column, rect)
        if self.tiles[row][column - 1] == 2:
            self.tiles[row][column - 1] = 0
            rect = smallest_rect(rect, pygame.rect.Rect((column-1) * self.tile_size, row * self.tile_size, self.tile_size,
                                                        self.tile_size))
            rect = self.breaking_glass(row, column - 1, rect)
        return rect

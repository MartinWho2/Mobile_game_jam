import pygame
import player


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
        self.gravity, self.friction = self.tile_size / 128, -0.2
        self.is_jumping = False
        self.max_speed = 10
        self.mask = pygame.mask.from_surface(self.image)
        self.flip_mask = 0
        self.tile = pygame.mask.Mask((self.tile_size, self.tile_size), fill=True)
        self.on_platform = False
        self.was_on_platform = 0
        self.map_size = [len(self.tiles), len(self.tiles[0])]

    def collide_with_mask(self, mask, pos_mask):
        return self.mask.overlap_mask(mask, (pos_mask[0] - self.rect.x, pos_mask[1] - self.rect.y))

    def check_collision(self, tiles=True, sprite_groups: [str, list] = "normal",return_sprite=False, breaking=False) -> list[
        pygame.mask.Mask]:
        if sprite_groups == "normal":
            sprite_groups = self.sprite_elements
        get_hits = []
        # Collision with tiles
        if tiles:
            # Checks for collisions with tiles near the sprite
            a = pygame.time.get_ticks()
            for r_index, row in enumerate(self.tiles):
                for c_index, item in enumerate(row):
                    tile = item
                    if tile != 0:
                        mask = self.collide_with_mask(self.tile, (c_index * self.tile_size, r_index * self.tile_size))
                        if mask.count():
                            if item == 2 and breaking:
                                self.tiles[r_index][c_index] = 0
                                self.breaking_glass(r_index, c_index)
                            else:
                                get_hits.append(mask)
            print(f"Collision with : map player {pygame.time.get_ticks()-a}")
        a = pygame.time.get_ticks()
        # Collision with elements
        for group in sprite_groups:
            for element in group:
                mask = self.collide_with_mask(element.mask, (element.rect.x, element.rect.y))
                if mask.count():
                    if return_sprite:
                        return element
                    get_hits.append(mask)
        print(f"Collision with sprites : player {pygame.time.get_ticks()-a}")
        return get_hits

    def collide(self, hits: list, axis: bool) -> int:
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
                    self.pos.y -= movement
                    self.is_jumping = False
                    if self.__class__ == player.Player:
                        if 'without_head' not in self.state:
                            self.state = 'idle'
                elif self.speed.y <= 0:
                    movement = self.find_bits_from_mask(mask, "up")
                    self.pos.y += movement
                self.speed.y = 0
                self.rect.y = round(self.pos.y)

            else:

                if self.speed.x > 0:
                    movement = self.find_bits_from_mask(mask, "right")
                    self.pos.x -= movement
                    movement = -movement
                elif self.speed.x <= 0:
                    movement = self.find_bits_from_mask(mask, "left")
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

    def fall(self, dt):
        self.pos.y += 0.5 * self.gravity * (dt ** 2) + self.speed.y * dt
        self.speed.y += self.gravity * dt
        self.rect.y = round(self.pos.y)
        hits = self.check_collision()
        self.collide(hits, True)

    def breaking_glass(self, row, column):
        if self.tiles[row + 1][column] == 2:
            self.tiles[row + 1][column] = 0
            self.breaking_glass(row + 1, column)
        if self.tiles[row][column + 1] == 2:
            self.tiles[row][column + 1] = 0
            self.breaking_glass(row, column + 1)
        if self.tiles[row - 1][column] == 2:
            self.tiles[row - 1][column] = 0
            self.breaking_glass(row - 1, column)
        if self.tiles[row][column - 1] == 2:
            self.tiles[row][column - 1] = 0
            self.breaking_glass(row, column - 1)

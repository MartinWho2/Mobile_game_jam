import math

import pygame


def draw_rounded_rect(surface: pygame.surface, rect, rect_color, bg_color, rounding=35):
    pygame.draw.rect(surface, rect_color, rect)
    quarter_circle = pygame.surface.Surface((rounding, rounding))
    quarter_circle.fill(bg_color)
    pygame.draw.circle(quarter_circle, rect_color, (rounding, rounding), rounding)
    surface.blit(quarter_circle, (rect.x, rect.y))
    quarter_circle = pygame.transform.rotate(quarter_circle, 90)
    surface.blit(quarter_circle, (rect.x, rect.bottom - rounding))
    quarter_circle = pygame.transform.rotate(quarter_circle, 90)
    surface.blit(quarter_circle, (rect.right - rounding, rect.bottom - rounding))
    quarter_circle = pygame.transform.rotate(quarter_circle, 90)
    surface.blit(quarter_circle, (rect.right - rounding, rect.y))
    return surface


def debug_print_mask(masks:list[pygame.mask.Mask]):
    for mask in masks:
        size = mask.get_size()
        for y in range(size[1]):
            for x in range(size[0]):
                print(mask.get_at((x,y)),end="")
            print("")
        print("END MASK\n\n")
def create_map(path: str, level: int) -> list:
    """
    Read a file and create a list corresponding to the map
    :param level: name of the file
    :return carte: map
    """
    filename = path + f"media/maps/level{level}.txt"
    # Order is up first and then clockwise
    with open(filename, "r") as file:
        text = file.read()
        carte = []
        temporary_list = []
        for char in text:
            if char != "\n":
                temporary_list.append(int(char))
            else:
                carte.append(temporary_list)
                temporary_list = []
        if temporary_list:
            carte.append(temporary_list)
        file.close()
    return carte

def show_mask(mask: pygame.mask.Mask):
    size = mask.get_size()
    for y in range(size[1]):
        for x in range(size[0]):
            print(mask.get_at((x,y)),end="")
        print()


def smallest_rect(rect1: pygame.rect.Rect, rect2: pygame.rect.Rect):
    rect = pygame.rect.Rect(min(rect1.x, rect2.x), min(rect1.y, rect2.y),
                            max(rect1.right, rect2.right) - min(rect1.x, rect2.x),
                            max(rect1.bottom, rect2.bottom)-min(rect1.y, rect2.y))
    return rect


def return_spritesheet(animations):
    output = []
    for idx, animation in enumerate(animations):
        output.append(animations[len(animations)-idx-1])
    return output


def get_tiles_from_rect(rect: pygame.rect.Rect, tile_size: int, max_size: tuple) -> list[tuple]:
    """
    Returns every tile contained in a rect within a list of tuples (y,x)
    This function assumes that a tile is a square.
    :param rect: The rect
    :param tile_size: The size of a tile
    :return:
    """
    tiles = []
    for x in range(math.floor(rect.x/tile_size), math.floor(rect.right/tile_size)+1):
        for y in range(math.floor(rect.y/tile_size), math.floor(rect.bottom/tile_size)+1):
            if x < max_size[0] and y < max_size[1]:
                tiles.append((y,x))
    return tiles


def rect_outside_of_rect2(rect:pygame.rect.Rect, rect2:pygame.rect.Rect) -> pygame.rect.Rect:
    if rect.bottom > rect2.bottom:
        return pygame.rect.Rect(rect.x,rect2.bottom,rect.w,rect.bottom-rect2.bottom)
    elif rect.y < rect2.y:
        return pygame.rect.Rect(rect.x,rect.y,rect.w,rect2.y-rect.y)
    elif rect.x < rect2.x:
        return pygame.rect.Rect(rect.x,rect.y,rect2.x-rect.x,rect.h)
    elif rect.right > rect2.right:
        return pygame.rect.Rect(rect2.right,rect.y,rect.right-rect2.right,rect.h)
    return False
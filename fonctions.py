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
                temporary_list.append(char)
            else:
                carte.append(temporary_list)
                temporary_list = []
        if temporary_list:
            carte.append(temporary_list)
        file.close()
    return carte



def return_spritesheet(animations):
    output = []
    for idx, animation in enumerate(animations):
        output.append(animations[len(animations)-idx-1])
    return output

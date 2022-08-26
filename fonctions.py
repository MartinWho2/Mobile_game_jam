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


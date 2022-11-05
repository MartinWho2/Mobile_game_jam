import pygame
from fonctions import draw_rounded_rect


class Interface_button(pygame.sprite.Sprite):
    def __init__(self, image: pygame.surface.Surface, pos: pygame.Vector2, size: int, name="", images=None):
        super().__init__()
        self.image = image
        self.rect = image.get_rect()
        self.image = pygame.transform.scale(self.image,(size,round(size*self.rect.h/self.rect.w)))
        self.rect = self.image.get_rect()
        self.image_clicked = pygame.transform.scale(self.image, (round(self.rect.w * 5/6),round(self.rect.h * 5/6)))
        self.image_clicked_rect = self.image_clicked.get_rect()
        self.clicking = False
        self.images = {False:self.image,True:self.image_clicked}
        self.rects = {False:self.rect,True:self.image_clicked_rect}
        self.rect.topleft = pos.xy
        self.image_clicked_rect.center = self.rect.center
        self.name = name
        self.button_state = False  # Only for button used for the arms and the vents: False if body, True if head
        if images:
            self.images_with_head = {"body":self.image,"head":pygame.transform.scale(images,(size,round(size*self.rect.h/self.rect.w)))}
            self.images_head_clicked = {False:self.images_with_head["head"],
                                        True:pygame.transform.scale(self.images_with_head["head"],
                                                                    (round(self.rect.w * 5/6),round(self.rect.h * 5/6)))}

    def click(self, state):
        self.clicking = state
        if self.button_state:
            self.image = self.images_head_clicked[self.clicking]
        else:
            self.image = self.images[self.clicking]
        self.rect = self.rects[self.clicking]

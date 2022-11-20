import pygame


class Interface_button(pygame.sprite.Sprite):
    def __init__(self, image: pygame.surface.Surface, pos: pygame.Vector2, size: int,
                 behind: pygame.surface.Surface, name="", images=None):
        super().__init__()
        self.image = image
        self.rect = image.get_rect()
        self.image = pygame.transform.scale(self.image, (size, round(size * self.rect.h / self.rect.w)))
        behind = pygame.transform.scale(behind, self.image.get_size())
        self.rect = self.image.get_rect()
        self.image_clicked = pygame.transform.scale(self.image,
                                                    (round(self.rect.w * 5 / 6), round(self.rect.h * 5 / 6)))
        behind_big = behind.copy()
        behind_copy = behind.copy()
        behind.blit(self.image, (0, 0))
        behind_big.blit(self.image_clicked, (round(self.rect.w / 12), round(self.rect.h / 12)))
        self.image = behind.copy()
        self.image_clicked = behind_big
        self.clicking = False
        self.images = {False: self.image, True: self.image_clicked}
        self.rect.topleft = pos.xy
        self.name = name
        self.button_state = False  # Only for button used for the arms and the vents: False if body, True if head
        if images:
            self.images_with_head = {"body": self.image,
                                     "head": pygame.transform.scale(images,
                                                                    (size, round(size * self.rect.h / self.rect.w)))}
            behind_head = behind_copy
            behind_head.blit(pygame.transform.scale(self.images_with_head["head"],
                                                    (round(self.rect.w * 5 / 6),
                                                     round(self.rect.h * 5 / 6))),
                             (round(self.rect.w / 12), round(self.rect.h / 12)))
            self.images_head_clicked = {False: self.images_with_head["head"],
                                        True: behind_head}

    def click(self, state, window: pygame.surface.Surface, offset: [int, int]):
        self.clicking = state
        if self.button_state:
            self.image = self.images_head_clicked[self.clicking]
        else:
            self.image = self.images[self.clicking]
        window.blit(self.image, (self.rect.x, self.rect.y))

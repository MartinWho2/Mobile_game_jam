import pygame
from interface_button import Interface_button


class Menu:
    def __init__(self, window, path:str):
        self.state = 1
        self.window = window
        self.font = pygame.font.SysFont('arial', 50)
        self.levels_buttons = []

        self.play_button = pygame.transform.scale(pygame.image.load(path+'media/button.png').convert_alpha(), (400, 100))
        self.play_button_rect = self.play_button.get_rect()
        self.play_text = self.font.render('PLAY', True, (150, 150, 150))
        self.play_text_rect = self.play_text.get_rect()
        self.play_text_rect.center = self.play_button_rect[2]/2, self.play_button_rect[3]/2
        self.play_button.blit(self.play_text, self.play_text_rect)
        self.play_button = Interface_button(self.play_button, pygame.Vector2(self.window.get_width()/4, self.window.get_height()/5), 400)

        self.options_button = pygame.transform.scale(pygame.image.load(path+'media/button.png').convert_alpha(), (400, 100))
        self.options_button_rect = self.options_button.get_rect()
        self.options_text = self.font.render('OPTIONS', True, (150, 150, 150))
        self.options_text_rect = self.options_text.get_rect()
        self.options_text_rect.center = self.options_button_rect[2]/2, self.options_button_rect[3]/2
        self.options_button.blit(self.options_text, self.options_text_rect)
        self.options_button = Interface_button(self.options_button, pygame.Vector2(self.window.get_width()/4, self.window.get_height()/5*2), 400)

        self.quit_button = pygame.transform.scale(pygame.image.load(path+'media/button.png').convert_alpha(), (400, 100))
        self.quit_button_rect = self.quit_button.get_rect()
        self.quit_text = self.font.render('QUIT', True, (150, 150, 150))
        self.quit_text_rect = self.quit_text.get_rect()
        self.quit_text_rect.center = self.quit_button_rect[2]/2, self.quit_button_rect[3]/2
        self.quit_button.blit(self.quit_text, self.quit_text_rect)
        self.quit_button = Interface_button(self.quit_button, pygame.Vector2(self.window.get_width()/4, self.window.get_height()/5*3), 400)

        self.back_button = pygame.transform.scale(pygame.image.load(path+'media/button.png').convert_alpha(), (400, 100))
        self.back_button_rect = self.back_button.get_rect()
        self.back_text = self.font.render('BACK', True, (150, 150, 150))
        self.back_text_rect = self.back_text.get_rect()
        self.back_text_rect.center = self.back_button_rect[2]/2, self.back_button_rect[3]/2
        self.back_button.blit(self.back_text, self.back_text_rect)
        self.back_button = Interface_button(self.back_button, pygame.Vector2(self.window.get_width()/8, self.window.get_height()/8*7), 400)

        for i in range(1, 9):
            button = pygame.transform.scale(pygame.image.load(path+'media/squared_button.png').convert_alpha(), (100, 100))
            button_rect = button.get_rect()
            button_rect.center = (self.window.get_width()/5*(i-4*int(i/4.5)), self.window.get_height()/4*(1+int(i/4.5)))
            text = self.font.render(f'{i}', True, (150, 150, 150))
            text_rect = text.get_rect()
            text_rect.center = button_rect[2]/2, button_rect[3]/2
            button.blit(text, text_rect)
            button = Interface_button(button, pygame.Vector2(self.window.get_width()/5*(i-4*int(i/4.5))-50, self.window.get_height()/4*(1+int(i/4.5))-50), 100)

            self.levels_buttons.append(button)

    def update(self):
        if self.state == 1:
            self.window.blit(self.play_button.image, self.play_button.rect)
            self.window.blit(self.options_button.image, self.options_button.rect)
            self.window.blit(self.quit_button.image, self.quit_button.rect)
        elif self.state == 2:
            for button in self.levels_buttons:
                self.window.blit(button.image, button.rect)

            self.window.blit(self.back_button.image, self.back_button.rect)
        elif self.state == 3:
            self.window.blit(self.back_button.image, self.back_button.rect)


import pygame
from interface_button import Interface_button


class Menu:
    def __init__(self, window, path:str, gradient:pygame.surface.Surface):
        self.state = 5
        self.window = window
        self.font = pygame.font.SysFont('arial', 50)
        self.levels_buttons = []

        self.open_screen = pygame.transform.scale(pygame.image.load(path+'media/open_screen.png').convert(), (self.window.get_width(), self.window.get_height()))
        self.open_screen_rect = self.open_screen.get_rect()
        self.win_image = pygame.transform.scale(pygame.image.load(path + 'media/win_image.png').convert(),
                                                (self.window.get_width(), self.window.get_height()))
        self.win_image_rect = self.win_image.get_rect()
        self.title_screen = pygame.transform.scale(pygame.image.load(path+"media/title_screen.png").convert(),self.window.get_size())

        self.play_button = pygame.transform.scale(pygame.image.load(path+'media/button.png').convert_alpha(), (400, 100))
        self.play_button_rect = self.play_button.get_rect()
        self.play_text = self.font.render('PLAY', True, (150, 150, 150))
        self.play_text_rect = self.play_text.get_rect()
        self.play_text_rect.center = self.play_button_rect[2]/2, self.play_button_rect[3]/2
        self.play_button.blit(self.play_text, self.play_text_rect)
        play_behind = self.play_button.copy()
        play_behind.blit(self.title_screen,(-self.window.get_width()/8, -self.window.get_height()/5-100))
        self.play_button = Interface_button(self.play_button,
                                            pygame.Vector2(self.window.get_width()/8, self.window.get_height()/5+100),
                                            400, play_behind)

        self.options_button = pygame.transform.scale(pygame.image.load(path+'media/button.png').convert_alpha(), (400, 100))
        self.options_button_rect = self.options_button.get_rect()
        self.options_text = self.font.render('OPTIONS', True, (150, 150, 150))
        self.options_text_rect = self.options_text.get_rect()
        self.options_text_rect.center = self.options_button_rect[2]/2, self.options_button_rect[3]/2
        self.options_button.blit(self.options_text, self.options_text_rect)
        options_behind = self.options_button.copy()
        options_behind.blit(self.title_screen,(-self.window.get_width()/8, -self.window.get_height()/5*2-100))
        self.options_button = Interface_button(self.options_button,
                                               pygame.Vector2(self.window.get_width()/8, self.window.get_height()/5*2+100),
                                               400, options_behind)

        self.quit_button = pygame.transform.scale(pygame.image.load(path+'media/button.png').convert_alpha(), (400, 100))
        self.quit_button_rect = self.quit_button.get_rect()
        self.quit_text = self.font.render('QUIT', True, (150, 150, 150))
        self.quit_text_rect = self.quit_text.get_rect()
        self.quit_text_rect.center = self.quit_button_rect[2]/2, self.quit_button_rect[3]/2
        self.quit_button.blit(self.quit_text, self.quit_text_rect)
        quit_behind = self.quit_button.copy()
        quit_behind.blit(self.title_screen,(-self.window.get_width()/8, -self.window.get_height()/5*3-100))
        self.quit_button = Interface_button(self.quit_button,
                                            pygame.Vector2(self.window.get_width()/8, self.window.get_height()/5*3+100),
                                            400, quit_behind)

        self.back_button = pygame.transform.scale(pygame.image.load(path+'media/button.png').convert_alpha(), (400, 100))
        self.back_button_rect = self.back_button.get_rect()
        self.back_text = self.font.render('BACK', True, (150, 150, 150))
        self.back_text_rect = self.back_text.get_rect()
        self.back_text_rect.center = self.back_button_rect[2]/2, self.back_button_rect[3]/2
        self.back_button.blit(self.back_text, self.back_text_rect)
        back_behind = self.back_button.copy()
        back_behind.blit(gradient, (0, -self.window.get_height()+100))
        self.back_button = Interface_button(self.back_button, pygame.Vector2(0, self.window.get_height()-100),
                                            400, back_behind)

        for i in range(1, 9):
            button = pygame.transform.scale(pygame.image.load(path+'media/squared_button.png').convert_alpha(), (150, 150))
            button_rect = button.get_rect()
            text = self.font.render(f'{i}', True, (150, 150, 150))
            text_rect = text.get_rect()
            text_rect.center = button_rect[2]/2, button_rect[3]/2
            button.blit(text, text_rect)
            button_behind = button.copy()
            button_behind.blit(gradient, (-self.window.get_width()/5*(i-4*int(i/4.5))+75,
                                          -self.window.get_height()/3*(1+int(i/4.5))+75))
            button = Interface_button(button, pygame.Vector2(self.window.get_width()/5*(i-4*int(i/4.5))-75,
                                                             self.window.get_height()/3*(1+int(i/4.5))-75), 150,
                                      button_behind)

            self.levels_buttons.append(button)

        self.resume_button = pygame.transform.scale(pygame.image.load(path + 'media/button.png').convert_alpha(),(400, 100))
        self.resume_button_rect = self.resume_button.get_rect()
        self.resume_text = self.font.render('RESUME', True, (150, 150, 150))
        self.resume_text_rect = self.resume_text.get_rect()
        self.resume_text_rect.center = self.play_button_rect[2] / 2, self.play_button_rect[3] / 2
        self.resume_button.blit(self.resume_text, self.resume_text_rect)
        resume_behind = self.resume_button.copy()
        resume_behind.blit(gradient,(-self.window.get_width() / 2+200, -self.window.get_height()/4))
        self.resume_button = Interface_button(self.resume_button,pygame.Vector2(self.window.get_width() / 2-200,
                                                                                self.window.get_height()/4),
                                              400, resume_behind)

        self.menu_button = pygame.transform.scale(pygame.image.load(path + 'media/button.png').convert_alpha(),(400, 100))
        self.menu_button_rect = self.menu_button.get_rect()
        self.menu_text = self.font.render('MAIN MENU', True, (150, 150, 150))
        self.menu_text_rect = self.menu_text.get_rect()
        self.menu_text_rect.center = self.play_button_rect[2] / 2, self.play_button_rect[3] / 2
        self.menu_button.blit(self.menu_text, self.menu_text_rect)
        menu_behind = self.menu_button.copy()
        menu_behind.blit(gradient,(-self.window.get_width() / 2+200, -self.window.get_height() / 4 * 2))
        self.menu_button = Interface_button(self.menu_button,pygame.Vector2(self.window.get_width() / 2-200,
                                                                            self.window.get_height() / 4*2),
                                            400,menu_behind)


        self.sound_text = self.font.render('Music:', True, (150, 150, 150))
        self.sound_text_rect = self.sound_text.get_rect()
        self.sound_text_rect.center = self.window.get_width()/3, self.window.get_height()/2
        self.sound_on_icon = pygame.image.load(path +'media/sound_on.png')
        self.sound_off_icon = pygame.image.load(path +'media/sound_off.png')
        self.sound_icon_rect = self.sound_on_icon.get_rect()
        self.sound_icon_rect.center = self.sound_text_rect.right+60, self.window.get_height()/2

        self.sound_clicked = False
        self.sound_state = True

    def update(self):
        if self.state == 1:
            self.window.blit(self.title_screen,(0,0))
            self.window.blit(self.play_button.image, self.play_button.rect)
            self.window.blit(self.options_button.image, self.options_button.rect)
            self.window.blit(self.quit_button.image, self.quit_button.rect)
        elif self.state == 2:
            for button in self.levels_buttons:
                self.window.blit(button.image, button.rect)
            self.window.blit(self.back_button.image, self.back_button.rect)
        elif self.state == 3:
            self.window.blit(self.sound_text, self.sound_text_rect)
            if self.sound_state:
                self.window.blit(self.sound_on_icon, self.sound_icon_rect)
            else:
                self.window.blit(self.sound_off_icon, self.sound_icon_rect)
            self.window.blit(self.back_button.image, self.back_button.rect)
        elif self.state == 4:
            self.window.blit(self.resume_button.image, self.resume_button.rect)
            self.window.blit(self.menu_button.image, self.menu_button.rect)
        elif self.state == 5:
            self.window.blit(self.open_screen, self.open_screen_rect)
        elif self.state == 6:
            self.window.blit(self.win_image, self.win_image_rect)

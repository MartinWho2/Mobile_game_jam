import pygame
from interface_button import Interface_button as Int_button

class Game():
    def __init__(self, window: pygame.surface.Surface, path:str):
        self.window = window
        self.w, self.h = self.window.get_size()
        arrow_right = pygame.image.load(path+"media/arrow.png").convert_alpha()
        arrow_up = pygame.image.load(path+"media/arrow_up.png")
        button = pygame.surface.Surface(arrow_right.get_size())
        button.fill((255,255,255))
        pygame.draw.rect(button,(128,128,128),arrow_right.get_rect(),width=1)
        jump_button = button.copy()
        jump_button.blit(arrow_up,(0,0))
        button.blit(arrow_right,(0,0))
        arrow_left = pygame.transform.flip(button,True,False)
        self.button_right = Int_button(button,pygame.Vector2(self.w/5,self.h*6/7),round(self.w/8),name="right")
        self.button_left = Int_button(arrow_left,pygame.Vector2(self.w/40,self.h*6/7),round(self.w/8),name="left")
        self.button_up = Int_button(jump_button,pygame.Vector2(self.w*6/7,self.h*6/7),round(self.w/8),name="up")
        square_button = pygame.transform.scale(pygame.image.load(path+'media/squared_button.png').convert_alpha(),(50,50))
        pause_button = square_button.copy()
        pause_image = pygame.transform.scale(pygame.image.load(path+'media/pause.png').convert_alpha(),(50,50))
        pause_button.blit(pause_image,(0,0))
        self.pause_button = Int_button(pause_button, pygame.Vector2(self.w-55, 5), 50,name="pause")
        self.level = 1
        self.buttons_interface = pygame.sprite.Group(self.button_right,self.button_left,self.button_up,self.pause_button)
        self.buttons = {self.button_left:False,self.button_right:False,self.button_up:False,self.pause_button:False}

    def update(self):
        for button in self.buttons_interface:
            self.window.blit(button.image, button.rect)


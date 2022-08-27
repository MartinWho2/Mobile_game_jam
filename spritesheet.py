import pygame
from fonctions import return_spritesheet

class Spritesheet:
    def __init__(self, character, path):
        # Single image size: image height
        self.number_of_frames = 0
        self.animations = {'idle': [],
                           'run_left': [],
                           'run_right': [],
                           'jump': []}
        self.frames_nrs = {'idle': 0,
                           'run_left': 0,
                           'run_right': 0,
                           'jump': 0}

        for animation in self.animations.keys():
            file_path = path + f'media/{character}/{animation}.png'
            img = pygame.image.load(file_path).convert_alpha()
            img_w = img.get_width()
            img_h = img.get_height()
            self.frames_nrs[animation] = int(img_w / img_h)
            imgs = []
            for x in range(0, self.frames_nrs[animation]):
                rect = pygame.rect.Rect(x * img_h, 0, img_h, img_h)
                imgs.append(img.subsurface(rect))
            if animation == 'run_left':
                imgs = return_spritesheet(imgs)
            self.animations[animation] = imgs

        self.frame_idx = 0
        self.animation_speed = 0.5

    def animate(self, state, dt):
        animation = self.animations[state]
        self.frame_idx += self.frames_nrs[state]/(dt*60)
        if self.frame_idx >= len(animation):
            self.frame_idx = 0
        return animation[int(self.frame_idx)]
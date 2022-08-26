import pygame


class Spritesheet:
    def __init__(self, character, tile_size):
        # Single image size: 48*48
        self.number_of_frames = 4
        self.animations = {'idle': [],
                           'run_left': [],
                           'run_right': [],
                           'jump': [],
                           'climb': []}

        for animation in self.animations.keys():
            path = f'media/{character}/{animation}.png'
            img = pygame.image.load(path).convert()
            imgs = []
            for x in range(0, self.number_of_frames):
                rect = pygame.rect.Rect(x * 48, 0, 48, 48)
                imgs.append(pygame.transform.scale(img.subsurface(rect), (tile_size*2, tile_size*2)))
            self.animations[animation] = imgs

        self.frame_idx = 0
        self.animation_speed = 0.1

    def animate(self, state, dt):
        animation = self.animations[state]
        self.frame_idx += self.animation_speed * dt
        if self.frame_idx >= len(animation):
            self.frame_idx = 0
        return animation[int(self.frame_idx)]
import pygame
import random

class Alien(pygame.sprite.Sprite):

    def __init__(self, width, height):
        super(Alien, self).__init__()
        self.w, self.h = width, height
        self.image = pygame.image.load('img/alien.png')
        self.rect = self.image.get_rect()
        self.screen_rect = width, height
        self.rect.centerx = random.randint(self.rect.width, self.w - self.rect.width)
        self.rect.centery = self.rect.height
        self.centery = float(self.rect.centery)
        self.centerx = float(self.rect.centerx)

        if bool(random.getrandbits(1)):
            self.mov_right = True
            self.mov_left = False
        else:
            self.mov_right = False
            self.mov_left = True

        self.mov_upwards = False
        self.mov_down = True


    def mov(self):
        if self.mov_right and self.rect.right < self.w:
            self.centerx += 1.5
        else:
            self.mov_right = False
            self.mov_left = True

        if self.mov_left and self.rect.left > 0:
            self.centerx -= 1.5
        else:
            self.mov_right = True
            self.mov_left = False

        if self.mov_down and self.rect.bottom < self.h:
            self.centery += 1.5
        else:
            self.mov_upwards = True
            self.mov_down = False

        if self.mov_upwards and self.rect.top > 0:
            self.centery -= 1.5
        else:
            self.mov_upwards = False
            self.mov_down = True

        self.rect.centerx = self.centerx
        self.rect.centery = self.centery

    def update(self):
        self.mov()
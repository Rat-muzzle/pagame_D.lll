import pygame
from pygame.locals import *


class Bird(pygame.sprite.Sprite):
    # функция вызываеться в первую очередь , при создании экземляра класса
    def __init__(self, x, y, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.w = width
        self.h = height

        self.images = []
        self.index = 0
        self.counter = 0
        for i in range(3):
            img = pygame.image.load(f'img/bird{i}.png')
            self.images.append(img)
        self.image = pygame.image.load('img/bird0.png')

        # создания хитбокса персонажа
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.centerx = float(self.rect.centerx)  # переменная которая хронит местоположение персонажа
        # она нам нужна , что бы хранить flot x или y
        # т.к rect.centerx(y) может быть только x , а мы хотим более плавное передвижение персонажа
        self.centery = float(self.rect.centery)  # тоже самое только для y
        # если переменные ниже True наж персонаж двигаеться туда где True

        # переменны птици
        self.mov_right = False
        self.mov_left = False
        self.mov_upwards = False
        self.mov_down = False

        # переменная отвечающая за полёт птици
        self.fly = False

    def mov(self):

        if self.fly == True:
            if self.mov_right and self.rect.right < self.w:
                # переменная которая хранить цент квадрата персонажа в float
                self.centerx += 3.5
            if self.mov_left and self.rect.left > 0:
                self.centerx -= 3.5
            if self.mov_upwards and self.rect.top > 0:
                self.centery -= 3.5
            if self.mov_down and self.rect.bottom < self.h:
                self.centery += 3.5

            # присвоение флоат значения квадрату главного персонажа
            self.rect.centerx = self.centerx
            self.rect.centery = self.centery


    def update(self):

        self.counter += 1
        # через какое количество фреймов игры обновляеться анимация птици
        if self.counter > 5:
            self.counter = 0
            self.index += 1
            if self.index >= len(self.images):
                self.index = 0
        self.image = self.images[self.index]

        self.mov()

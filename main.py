from bird import Bird
from enemy import Alien
import save_date
import pygame
from pygame.locals import *
import time

pygame.init()

# ограничение кадров игры (игровых тиков)
clock = pygame.time.Clock()
fps = 60
pipi_time_creature = 2000
last_time = pygame.time.get_ticks()

# создаём игровой экран
width = 864
height = 736
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('выжить 10 секунд')

# загрузка картинок
bg = pygame.image.load('img/bg.png')

# создаём группу , где мы будем хранить спрайты(экземпляр класса bird) птици
bird_group = pygame.sprite.Group()
# создаём экземпляр класса bird
bird = Bird(width // 2, height // 2, width, height)
# добовляем экземпляр класса в группу спрайтов
bird_group.add(bird)

# создаём врага
alien_group = pygame.sprite.Group()
alien = Alien(width, height)
alien_group.add(alien)

game_over = False
game = None

BLUE = '#0000ff'
RED = '#B22222'

# время
pygame.time.set_timer(pygame.USEREVENT, 1000)
text_time = 0
font_name = pygame.font.SysFont(None, 48)
time_clock = font_name.render(f'{text_time}', True, RED)
clock = pygame.time.Clock()

# приветственные слова
font_greeting_1 = pygame.font.SysFont(None, 60)
greeting1 = font_greeting_1.render('Hello', True, BLUE)

font_greeting_2 = pygame.font.SysFont(None, 30)
greeting2 = font_greeting_2.render('the game is in alpha test', True, BLUE)
greeting3 = font_greeting_2.render('If you liked her , you "re weird', True, BLUE)
greeting4 = font_greeting_2.render('write your name and press ENTER', True, RED)

# ввод имени
text = ''
font_name = pygame.font.SysFont(None, 48)
name = font_name.render(text, True, RED)

# последнии слова
font_lose = pygame.font.SysFont(None, 75)
lose = font_lose.render('END GAME', True, RED)
win = font_lose.render('WIN GAME', True, RED)
win2 = font_lose.render('list game winers', True, RED)

rect = name.get_rect()
rect.topleft = (width // 3, height // 2 - 120)
cursor = Rect(rect.topright, (3, rect.height))

# вызваем проверку создание бд
save_date.baze_start()

while True:

    clock.tick(fps)
    # отрисовываем задний фон
    screen.blit(bg, (0, 0))

    # if bird.rect.bottom > 768:
    #     game_over = True
    #     bird.fly = False

    bird_group.draw(screen)
    bird_group.update()
    if bird.fly == True:
        alien_group.draw(screen)
        alien_group.update()
    # if not game_over and bird.fly:
    #     time_ct = pygame.time.get_ticks()
    #     if time_ct - last_time > pipi_time_creature:
    #         pipi_h = random.randint(-150, 150)
    #         pipi1 = Pipi(width + 100, (height // 2) + pipi_h, 1)
    #         pipi2 = Pipi(width + 100, (height // 2) + pipi_h, 0)
    #         pipi_group.add(pipi1)
    #         pipi_group.add(pipi2)
    #         last_time = pygame.time.get_ticks()

    # обработка всех событий в игре
    for event in pygame.event.get():
        # если игровое событие == выход из игры , выходим из игры
        if event.type == QUIT:
            pygame.quit()
        # запуск игры
        if event.type == KEYDOWN and bird.fly == False:
            if event.key == K_RETURN and len(text) > 0:
                bird.fly = True

        # работаем с именем
        if bird.fly == False and game_over == False:
            if event.type == KEYDOWN:
                if event.key == K_BACKSPACE:
                    if len(text) > 0:
                        text = text[:-1]
                else:
                    text += event.unicode
                name = font_name.render(text, True, RED)
                rect.size = name.get_size()
                cursor.topleft = rect.topright
        # работа с временем
        if bird.fly == True and game_over == False:
            if event.type == pygame.USEREVENT:
                text_time += 1

        if event.type == KEYDOWN:
            if event.key == K_RIGHT:
                bird.mov_right = True
            elif event.key == K_LEFT:
                bird.mov_left = True
            elif event.key == K_UP:
                bird.mov_upwards = True
            elif event.key == K_DOWN:
                bird.mov_down = True

        if event.type == KEYUP:
            if event.key == K_RIGHT:
                bird.mov_right = False
            elif event.key == K_LEFT:
                bird.mov_left = False
            elif event.key == K_UP:
                bird.mov_upwards = False
            elif event.key == K_DOWN:
                bird.mov_down = False

    # обновление экрана игры
    # screen.blit(ground, (ground_scroll, 768))

    # создаём текст
    if bird.fly == False and game_over == False:

        # приветственные слова
        screen.blit(greeting1, (100, 100))
        screen.blit(greeting2, (100, 150))
        screen.blit(greeting3, (100, 180))
        screen.blit(greeting4, (width // 3, height // 2 - 150))

        screen.blit(name, rect)
        if time.time() % 1 > 0.5:
            pygame.draw.rect(screen, RED, cursor)
        pygame.display.update()
    else:
        time_clock = font_name.render(f'{text_time}', True, RED)
        screen.blit(time_clock, (100, 100))
    # концовка игры
    if game_over == True:
        if game == 'lose_game':
            screen.blit(lose, (width // 2, height // 2))
        elif game == 'win_game':
            screen.blit(win, (width // 2, height // 2))
            screen.blit(win2, (width // 6, 300 - 55))
            font_lose = pygame.font.SysFont(None, 75)
            n = 0
            for i in win_list:
                n += 55
                win_l = font_lose.render(f'{i[0]}', True, RED)
                screen.blit(win_l, (width // 6, 300 + n))
            pass

    if pygame.sprite.groupcollide(bird_group, alien_group, True, False) and game_over == False:
        game = 'lose_game'
        game_over = True

    if text_time >= 10 and game_over == False:
        game = 'win_game'
        save_date.add_pleer(text, text_time)
        for i in alien_group:
            alien_group.remove(i)
        win_list = save_date.crate_win_list()
        game_over = True

    pygame.display.update()

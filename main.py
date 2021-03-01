#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Creates Tanks game.

It just realises a game with tanks in Python using PyGame module.
"""

import math
import os
import random
import sys

import pygame

__author__ = ["Ilya B. Anosov", "Sofia P. Kalinina"]
__credits__ = ["Georgiy A. Darovskih"]
__version__ = "1.0.1"
__maintainer__ = ["Ilya B. Anosov"]
__email__ = "anosovilya465@yandex.ru"
__status__ = "Development"

RED = pygame.Color('red')
GREEN = pygame.Color('green')
BLUE = pygame.Color('blue')

BLACK = pygame.Color('black')
WHITE = pygame.Color('white')

YELLOW = pygame.Color('yellow')

current_turret_pos = 0
ANGLES = {
    0: math.radians(5), 1: math.radians(15), 2: math.radians(25),
    3: math.radians(35), 4: math.radians(45), 5: math.radians(55),
    6: math.radians(65), 7: math.radians(75), 8: math.radians(85)
}

# noinspection PyBroadException
try:
    args = sys.argv[1:]
    filename = args[0]
    filename = 'data/' + filename
    if not os.path.exists(filename):
        raise FileNotFoundError
except Exception:
    print('Такого файла не существует')
    sys.exit(0)


def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Не удаётся загрузить:', name)
        raise SystemExit(message)
    image = image.convert_alpha()
    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    return image


class ScreenFrame(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.rect = 0, 0, 500, 500


class SpriteGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

    def get_event(self, event):
        for sprite in self:
            sprite.get_event(event)


class Sprite(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.rect = None

    def get_event(self, event):
        pass


class Tile(Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(sprite_group)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x,
                                               tile_height * pos_y)


class Player(Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(hero_group)
        self.image = player_image
        self.rect = self.image.get_rect().move(tile_width * pos_x + 15,
                                               tile_height * pos_y + 5)
        screen.blit(background_image, (0, 0))
        x = pos_x * tile_width + 40
        y = pos_y * tile_height + 15
        possibleTurrets = [
            (x - 27, y - 2),
            (x - 26, y - 5),
            (x - 25, y - 8),
            (x - 23, y - 12),
            (x - 20, y - 14),
            (x - 18, y - 15),
            (x - 15, y - 17),
            (x - 13, y - 19),
            (x - 11, y - 21)
        ]
        pygame.draw.line(screen, pygame.color.Color('darkgreen'),
                         (tile_width * pos_x + 40,
                          tile_height * pos_y + 15),
                         possibleTurrets[current_turret_pos], 5)

        self.pos = (pos_x, pos_y)

    def move(self, x, y):
        self.pos = (x, y)
        self.rect = self.image.get_rect().move(tile_width * self.pos[0] + 15,
                                               tile_height * self.pos[1] + 5)
        x = x * tile_width + 40
        y = y * tile_height + 15
        screen.blit(background_image, (0, 0))
        possibleTurrets = [
            (x - 27, y - 2),
            (x - 26, y - 5),
            (x - 25, y - 8),
            (x - 23, y - 12),
            (x - 20, y - 14),
            (x - 18, y - 15),
            (x - 15, y - 17),
            (x - 13, y - 19),
            (x - 11, y - 21)
        ]
        pygame.draw.line(screen, pygame.color.Color('darkgreen'),
                         (tile_width * self.pos[0] + 40,
                          tile_height * self.pos[1] + 15),
                         possibleTurrets[current_turret_pos], 5)


class Bullet(Sprite):
    def __init__(self, x, y):
        super().__init__(bullet_group)
        self.image = pygame.Surface((10, 20))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

        pygame.draw.circle(screen, RED, (x, y), radius=5)


def terminate():
    pygame.quit()
    sys.exit(0)


def start_screen():
    background = pygame.transform.scale(load_image('intro.jpg'), size)
    screen.blit(background, (0, 0))

    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    intro = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit(0)

        show_message('Tanks. Shoot-out',
                     pygame.Color('white'), -175, size='large')
        show_message('Порази противника первым.',
                     pygame.Color('white'), -90)

        create_button('Играть', 200, 515, 150, 50,
                      BLACK, GREEN, action='play')
        create_button('Управление', 400, 515, 200, 50,
                      BLACK, YELLOW, action='controls')
        create_button('Выйти', 650, 515, 150, 50,
                      BLACK, RED, action='quit')

        # смена (отрисовка) кадра:
        pygame.display.flip()
        clock.tick(FPS)


def game_controls():
    background = pygame.transform.scale(load_image('intro.jpg'), size)
    screen.blit(background, (0, 0))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)

        show_message('Управление:', WHITE, -175, size='large')
        show_message('Выстрел: [пробел]', WHITE, -90)
        show_message('Движение пушки: [↑], [↓]', WHITE, -50)
        show_message('Движение танка: [←], [→]', WHITE, -10)
        show_message('Увеличение скорости выстрела: [D]', WHITE, 30)
        show_message('Уменьшение скорости выстрела: [A]', WHITE, 70)
        show_message('Пауза: [P]', WHITE, 110)

        create_button('Играть', 200, 515, 150, 50,
                      BLACK, GREEN, action='play')
        create_button('На главную', 400, 515, 200, 50,
                      BLACK, YELLOW, action='main')
        create_button('Выйти', 650, 515, 150, 50,
                      BLACK, RED, action='quit')

        # смена (отрисовка) кадра:
        pygame.display.flip()
        clock.tick(FPS)


def pause():
    paused = True
    show_message('Пауза!', BLACK, -100, size='large')
    show_message('Нажмите [C] для продолжения.',
                 BLACK, 10)
    show_message('Нажмите [Q], чтобы выйти из игры.',
                 BLACK, 50)

    # смена (отрисовка) кадра:
    pygame.display.flip()

    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    paused = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit(0)
        clock.tick(FPS)


def text_objects(text, color, size='small'):
    if size == 'small':
        surf = small_font.render(text, True, color)
    elif size == 'medium':
        surf = medium_font.render(text, True, color)
    elif size == 'large':
        surf = large_font.render(text, True, color)
    return surf, surf.get_rect()


def text_to_button(msg, color, x, y, w, h, size='small'):
    surf, rect = text_objects(msg, color, size)
    rect.center = ((x + (w / 2)), y + (h / 2))
    screen.blit(surf, rect)


def create_button(text, x, y, w, h, inactive_color, active_color, action=None):
    cur = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x + w > cur[0] > x and y + h > cur[1] > y:
        pygame.draw.rect(screen, active_color, (x, y, w, h))
        text_to_button(text, BLACK, x, y, w, h)
        if click[0] == 1 and action is not None:
            if action == 'quit':
                pygame.quit()
                sys.exit(0)
            if action == 'controls':
                game_controls()
            if action == 'play':
                main()
            if action == 'main':
                start_screen()
    else:
        pygame.draw.rect(screen, inactive_color, (x, y, w, h))
        text_to_button(text, WHITE, x, y, w, h)


def show_message(msg, color, y=0, size='small'):
    surf, rect = text_objects(msg, color, size)
    rect.center = (int(width / 2), int(height / 2) + y)
    screen.blit(surf, rect)


def load_level(filename):
    # читаем уровень, убирая символы перевода строки
    with open(filename, mode='r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: list(x.ljust(max_width, '.')), level_map))


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
                level[y][x] = '.'
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y


def main():
    def move(hero, movement):
        global current_turret_pos
        global filename
        x, y = hero.pos
        if movement == 'up':
            current_turret_pos += 1 if current_turret_pos < 8 else 0
            hero.move(x, y)
        elif movement == 'down':
            current_turret_pos -= 1 if current_turret_pos > 0 else 0
            hero.move(x, y)
        elif movement == 'left':
            if x > 0 and level_map[y][x - 1] == '.':
                hero.move(x - 1, y)
        elif movement == 'right':
            if x < max_x - 1 and level_map[y][x + 1] == '.':
                hero.move(x + 1, y)

    level_map = load_level(filename)
    hero, max_x, max_y = generate_level(level_map)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pause()
                elif event.key == pygame.K_UP:
                    move(hero, 'up')
                elif event.key == pygame.K_DOWN:
                    move(hero, 'down')
                elif event.key == pygame.K_LEFT:
                    move(hero, 'left')
                elif event.key == pygame.K_RIGHT:
                    move(hero, 'right')
                elif event.key == pygame.K_SPACE:
                    while True:
                        bullet = Bullet(300, 300)

            elif event.type == pygame.ACTIVEEVENT:
                if event.gain == 0 and event.state == 2:
                    pause()

        sprite_group.draw(screen)
        hero_group.draw(screen)
        bullet_group.draw(screen)

        clock.tick(FPS)
        # смена (отрисовка) кадра:
        pygame.display.flip()

    # завершение работы:
    pygame.quit()


if __name__ == '__main__':
    # инициализация Pygame:
    pygame.init()
    pygame.display.set_caption('Tanks. Shoot-out')
    # размеры окна:
    # noinspection PyUnboundLocalVariable
    size = width, height = 1000, 600
    # screen — холст, на котором нужно рисовать:
    screen = pygame.display.set_mode(size)

    FPS = 50
    tile_width = tile_height = 50

    small_font = pygame.font.SysFont('Menlo', 24)
    medium_font = pygame.font.SysFont('Menlo', 48)
    large_font = pygame.font.SysFont('Menlo', 72)

    tile_images = {
        'wall': load_image('ground.jpg'),
        'empty': load_image('empty.png')
    }
    player_image = load_image('tank.png')
    player_image = pygame.transform.scale(player_image, (80, 45))

    background_image = pygame.image.load('data/background.jpg').convert()
    background_image = pygame.transform.scale(background_image,
                                              (width, height))

    # основной персонаж
    player = None

    # группы спрайтов
    sprite_group = SpriteGroup()
    hero_group = SpriteGroup()
    bullet_group = SpriteGroup()

    clock = pygame.time.Clock()

    start_screen()

#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Creates Tanks game.

It just realises a game with tanks in Python using PyGame module.
"""

import argparse
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
__status__ = "Production"

RED = pygame.Color('red')
GREEN = pygame.Color('green')
BLUE = pygame.Color('blue')

BLACK = pygame.Color('black')
WHITE = pygame.Color('white')

YELLOW = pygame.Color('yellow')

RED3 = pygame.Color('red3')
YELLOW3 = pygame.Color('yellow3')

DARK_GREEN = pygame.Color('darkgreen')

PLAYER_SHIFT_X = 45
PLAYER_SHIFT_Y = -10

ENEMY_SHIFT_X = 85
ENEMY_SHIFT_Y = -10

ANGLES = {
    0: math.radians(5), 1: math.radians(15), 2: math.radians(25),
    3: math.radians(35), 4: math.radians(45), 5: math.radians(55),
    6: math.radians(65), 7: math.radians(75), 8: math.radians(85)
}

current_player_turret_pos = 0
current_enemy_turret_pos = 0

parser = argparse.ArgumentParser()
parser.add_argument('filename', metavar='filename', nargs='*',
                    type=str, default=['map.txt'],
                    help='map file name')

args = parser.parse_args()
filename = args.filename[0]

# noinspection PyBroadException
try:
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
        self.rect = pygame.rect.Rect(0, 0, 1000, 600)


class SpriteGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

    def get_event(self, event):
        for sprite in self:
            # noinspection PyUnresolvedReferences
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


class Block(Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(block_group)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x,
                                               tile_height * pos_y)


class Player(Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(hero_group)
        self.health = 100
        player_health_bar(self.health)
        for enemy in enemy_group:
            enemy_health_bar(enemy.health, enemy.health_pos_x)
        self.image = player_image
        self.rect = self.image.get_rect().move(tile_width * pos_x + 25,
                                               tile_height * (pos_y - 1) + 5)
        # screen.blit(background_image, (0, 0))
        x = pos_x * tile_width + PLAYER_SHIFT_X
        y = pos_y * tile_height + PLAYER_SHIFT_Y
        available_pos = [
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
        pygame.draw.line(screen, DARK_GREEN,
                         (tile_width * pos_x + PLAYER_SHIFT_X,
                          tile_height * pos_y + PLAYER_SHIFT_Y),
                         available_pos[current_player_turret_pos], 5)

        self.pos = (pos_x, pos_y)

    def move(self, x, y):
        player_health_bar(self.health)
        for enemy in enemy_group:
            enemy_health_bar(enemy.health, enemy.health_pos_x)
        self.pos = (x, y)
        self.rect = self.image.get_rect().move(
            tile_width * self.pos[0] + 25,
            tile_height * (self.pos[1] - 1) + 5)
        x = x * tile_width + PLAYER_SHIFT_X
        y = y * tile_height + PLAYER_SHIFT_Y
        # screen.blit(background_image, (0, 0))
        available_pos = [
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
        pygame.draw.line(screen, DARK_GREEN,
                         (tile_width * self.pos[0] + PLAYER_SHIFT_X,
                          tile_height * self.pos[1] + PLAYER_SHIFT_Y),
                         available_pos[current_player_turret_pos], 5)


class Enemy(Sprite):
    def __init__(self, pos_x, pos_y, health_pos_x):
        super().__init__(enemy_group)
        self.health = 100
        self.health_pos_x = health_pos_x
        for enemy in enemy_group:
            enemy_health_bar(enemy.health, enemy.health_pos_x)
        self.image = enemy_image
        self.rect = self.image.get_rect().move(tile_width * pos_x + 25,
                                               tile_height * (pos_y - 1) + 5)
        # screen.blit(background_image, (0, 0))
        x = pos_x * tile_width + ENEMY_SHIFT_X
        y = pos_y * tile_height + ENEMY_SHIFT_Y
        available_pos = [
            (x + 27, y - 2),
            (x + 26, y - 5),
            (x + 25, y - 8),
            (x + 23, y - 12),
            (x + 20, y - 14),
            (x + 18, y - 15),
            (x + 15, y - 17),
            (x + 13, y - 19),
            (x + 11, y - 21)
        ]
        pygame.draw.line(screen, DARK_GREEN,
                         (tile_width * pos_x + ENEMY_SHIFT_X,
                          tile_height * pos_y + ENEMY_SHIFT_Y),
                         available_pos[current_enemy_turret_pos], 5)

        self.pos = (pos_x, pos_y)

    def move(self, x, y):
        for enemy in enemy_group:
            enemy_health_bar(enemy.health, enemy.health_pos_x)
        self.pos = (x, y)
        self.rect = self.image.get_rect().move(
            tile_width * self.pos[0] + 25,
            tile_height * (self.pos[1] - 1) + 5)
        x = x * tile_width + ENEMY_SHIFT_X
        y = y * tile_height + ENEMY_SHIFT_Y
        # screen.blit(background_image, (0, 0))
        available_pos = [
            (x + 27, y - 2),
            (x + 26, y - 5),
            (x + 25, y - 8),
            (x + 23, y - 12),
            (x + 20, y - 14),
            (x + 18, y - 15),
            (x + 15, y - 17),
            (x + 13, y - 19),
            (x + 11, y - 21)
        ]
        pygame.draw.line(screen, DARK_GREEN,
                         (tile_width * self.pos[0] + ENEMY_SHIFT_X,
                          tile_height * self.pos[1] + ENEMY_SHIFT_Y),
                         available_pos[current_enemy_turret_pos], 5)


class Bullet(Sprite):
    def __init__(self, x, y):
        super().__init__(bullet_group)
        self.image = bomb_image
        self.rect = self.image.get_rect().move(x, y)
        self.pos = (x, y)

    def render(self, x, y):
        self.rect = self.image.get_rect().move(x, y)
        self.pos = (x, y)


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
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    intro = False
                elif event.key == pygame.K_q:
                    terminate()

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
                terminate()

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
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    paused = False
                elif event.key == pygame.K_q:
                    terminate()
        clock.tick(FPS)


def game_over():
    is_over = True
    show_message('Вы проиграли!', BLACK, -100, size='large')
    show_message('Нажмите [Q], чтобы выйти из игры.',
                 BLACK, 10)

    # смена (отрисовка) кадра:
    pygame.display.flip()

    while is_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    terminate()
        clock.tick(FPS)


def victory():
    is_victory = True
    show_message('Вы выиграли!', BLACK, -100, size='large')
    show_message('Нажмите [Q], чтобы выйти из игры.',
                 BLACK, 10)

    # смена (отрисовка) кадра:
    pygame.display.flip()

    while is_victory:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    terminate()
        clock.tick(FPS)


# noinspection PyShadowingNames
def text_objects(text, color, size='small'):
    if size == 'small':
        surf = small_font.render(text, True, color)
    elif size == 'medium':
        surf = medium_font.render(text, True, color)
    elif size == 'large':
        surf = large_font.render(text, True, color)
    # noinspection PyUnboundLocalVariable
    return surf, surf.get_rect()


# noinspection PyShadowingNames
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
                terminate()
            if action == 'controls':
                game_controls()
            if action == 'play':
                main()
            if action == 'main':
                start_screen()
    else:
        pygame.draw.rect(screen, inactive_color, (x, y, w, h))
        text_to_button(text, WHITE, x, y, w, h)


# noinspection PyShadowingNames
def show_message(msg, color, y=0, size='small'):
    surf, rect = text_objects(msg, color, size)
    rect.center = (int(width / 2), int(height / 2) + y)
    screen.blit(surf, rect)


# noinspection PyShadowingNames
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
    health_x = 21
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Block('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
                level[y][x] = '.'
            elif level[y][x] == '*':
                Tile('empty', x, y)
                Enemy(x, y, health_x)
                level[y][x] = '.'
                health_x += 28 + 10
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y


def player_health_bar(player_health):
    if player_health >= 80:
        player_health_color = GREEN
    elif player_health >= 40:
        player_health_color = YELLOW
    else:
        player_health_color = RED

    pygame.draw.rect(screen, BLACK,
                     (780, 21, 103, 28), 2)
    pygame.draw.rect(screen, player_health_color,
                     (782, 22, player_health, 25))


def enemy_health_bar(enemy_health, x):
    if enemy_health >= 80:
        player_health_color = GREEN
    elif enemy_health >= 40:
        player_health_color = YELLOW
    else:
        player_health_color = RED

    pygame.draw.rect(screen, BLACK,
                     (120, x, 103, 28), 2)
    pygame.draw.rect(screen, player_health_color,
                     (122, x + 1, enemy_health, 25))


def main():
    global current_player_turret_pos
    global current_enemy_turret_pos
    global power

    # noinspection PyShadowingNames
    def move(hero, movement):
        global current_player_turret_pos
        global filename
        x, y = hero.pos
        if movement == 'up':
            current_player_turret_pos += 1 if \
                current_player_turret_pos < 8 else 0
            hero.move(x, y)
        elif movement == 'down':
            current_player_turret_pos -= 1 if \
                current_player_turret_pos > 0 else 0
            hero.move(x, y)
        elif movement == 'left':
            if hero.rect.left >= tile_width:
                if x > 0 and level_map[y][x - 1] == '.':
                    hero.move(x - 1, y)
        elif movement == 'right':
            if hero.rect.right <= width - tile_width:
                if x < max_x - 1 and x < max_x - 4 and \
                        level_map[y][x + 1] != '#' and \
                        level_map[y][x + 2] != '#' and \
                        level_map[y][x + 3] != '#' and \
                        level_map[y][x + 4] != '#':
                    hero.move(x + 1, y)

    def explosion(explode_x, explode_y,
                  max_magnitude=(tile_width + tile_height) / 2):
        colors = [RED, RED3, YELLOW, YELLOW3]
        magnitude = 1

        exploding = True
        while exploding:
            # noinspection PyShadowingNames
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()

            while magnitude < 1.5 * max_magnitude:
                explode_x_ = explode_x + random.randrange(
                    -magnitude, magnitude)
                explode_y_ = explode_y + random.randrange(
                    -magnitude, magnitude)

                pygame.draw.circle(screen, colors[random.randrange(0, 4)],
                                   (explode_x_, explode_y_),
                                   random.randrange(1, 7))
                magnitude += 1

                clock.tick(FPS)
                # смена (отрисовка) кадра:
                pygame.display.flip()

            exploding = False

    # noinspection PyUnboundLocalVariable
    level_map = load_level(filename)
    hero, max_x, max_y = generate_level(level_map)

    running = True
    while running:
        if not enemy_group:
            victory()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pause()

                elif event.key == pygame.K_a:
                    power -= 1
                    if power < 1:
                        power = 1
                elif event.key == pygame.K_d:
                    power += 1
                    if power > 99:
                        power = 99

                elif event.key == pygame.K_UP:
                    move(hero, 'up')
                elif event.key == pygame.K_DOWN:
                    move(hero, 'down')
                elif event.key == pygame.K_LEFT:
                    move(hero, 'left')
                elif event.key == pygame.K_RIGHT:
                    move(hero, 'right')

                elif event.key == pygame.K_SPACE:
                    for enemy in enemy_group:
                        enemy.move(*enemy.pos)
                    x = hero.pos[0] * tile_width + PLAYER_SHIFT_X
                    y = hero.pos[1] * tile_height + PLAYER_SHIFT_Y
                    available_pos = [
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
                    x = available_pos[current_player_turret_pos][0] - 5
                    y = available_pos[current_player_turret_pos][1] - 3

                    x_y = [x, y]

                    fire = True
                    pygame.mixer.Sound.play(fire_sound)
                    while fire:
                        bullet = Bullet(x_y[0], x_y[1])
                        x_y[0] -= (10 - current_player_turret_pos) * 2
                        x_y[1] += int(
                            (((x_y[0] - x) * 0.015 / (power / 50)) ** 2) -
                            (current_player_turret_pos +
                             current_player_turret_pos /
                             (10 - current_player_turret_pos)))
                        bullet_group.draw(screen)

                        if pygame.sprite.spritecollide(
                                bullet, block_group, dokill=False) or \
                                pygame.sprite.spritecollide(
                                    bullet, enemy_group, dokill=False):
                            if pygame.sprite.spritecollide(
                                    bullet, enemy_group, dokill=False):
                                for enemy in enemy_group:
                                    enemy_health_bar(enemy.health,
                                                     enemy.health_pos_x)
                                    if pygame.sprite.spritecollide(
                                            enemy, bullet_group, dokill=False):
                                        if enemy.health:
                                            enemy.health -= 20
                                        else:
                                            enemy.kill()
                            explosion(*x_y)
                            pygame.time.wait(1000)
                            for sprite in bullet_group:
                                sprite.kill()
                            hero.move(*hero.pos)
                            fire = False

                    # -------------------------------------------------

                    for enemy in enemy_group:
                        for i in range(random.randint(1, 5)):
                            move(enemy, random.choice(['left', 'right']))

                        screen.blit(background_image, (0, 0))
                        hero.move(*hero.pos)
                        enemy.move(*enemy.pos)
                        sprite_group.draw(screen)
                        block_group.draw(screen)
                        hero_group.draw(screen)
                        enemy_group.draw(screen)
                        bullet_group.draw(screen)

                    # -------------------------------------------------

                    for enemy in enemy_group:
                        current_enemy_turret_pos = random.randint(3, 8)
                        enemy_power = random.randint(50, 99)

                        screen.blit(background_image, (0, 0))
                        for enemy_sprite in enemy_group:
                            enemy_sprite.move(*enemy_sprite.pos)
                        enemy.move(*enemy.pos)
                        hero.move(*hero.pos)
                        sprite_group.draw(screen)
                        block_group.draw(screen)
                        hero_group.draw(screen)
                        enemy_group.draw(screen)
                        bullet_group.draw(screen)

                        x = enemy.pos[0] * tile_width + ENEMY_SHIFT_X
                        y = enemy.pos[1] * tile_height + ENEMY_SHIFT_Y
                        available_pos = [
                            (x + 27, y - 2),
                            (x + 26, y - 5),
                            (x + 25, y - 8),
                            (x + 23, y - 12),
                            (x + 20, y - 14),
                            (x + 18, y - 15),
                            (x + 15, y - 17),
                            (x + 13, y - 19),
                            (x + 11, y - 21)
                        ]
                        x = available_pos[current_enemy_turret_pos][0] - 5
                        y = available_pos[current_enemy_turret_pos][1] - 3

                        x_y = [x, y]

                        fire = True
                        pygame.mixer.Sound.play(fire_sound)
                        while fire:
                            bullet = Bullet(x_y[0], x_y[1])
                            x_y[0] += (10 - current_enemy_turret_pos) * 2
                            x_y[1] += int(
                                (((x_y[0] - x) * 0.015 /
                                  (enemy_power / 50)) ** 2) -
                                (current_enemy_turret_pos +
                                 current_enemy_turret_pos /
                                 (10 - current_enemy_turret_pos)))
                            bullet_group.draw(screen)

                            if pygame.sprite.spritecollide(
                                    bullet, block_group, dokill=False) or \
                                    pygame.sprite.spritecollide(
                                        bullet, hero_group, dokill=False):
                                if pygame.sprite.spritecollide(
                                        bullet, hero_group, dokill=False):
                                    for hero in hero_group:
                                        if pygame.sprite.spritecollide(
                                                hero, bullet_group,
                                                dokill=False):
                                            if hero.health:
                                                hero.health -= 20
                                            else:
                                                game_over()
                                explosion(*x_y)
                                pygame.time.wait(1000)
                                for sprite in bullet_group:
                                    sprite.kill()
                                fire = False

            elif event.type == pygame.ACTIVEEVENT:
                if event.gain == 0 and event.state == 2:
                    pause()

        screen.blit(background_image, (0, 0))
        hero.move(*hero.pos)
        for sprite in enemy_group:
            # noinspection PyUnresolvedReferences
            sprite.move(*sprite.pos)
        show_message(f'Мощность выстрела: {power}%', BLACK, -270,
                     size='small')

        sprite_group.draw(screen)
        block_group.draw(screen)
        hero_group.draw(screen)
        enemy_group.draw(screen)
        bullet_group.draw(screen)

        for enemy in enemy_group:
            enemy_health_bar(enemy.health, enemy.health_pos_x)

        clock.tick(FPS)
        # смена (отрисовка) кадра:
        pygame.display.flip()

    # завершение работы:
    pygame.quit()


if __name__ == '__main__':
    # инициализация Pygame:
    pygame.init()
    pygame.display.set_caption('Tanks. Shoot-out')

    icon = pygame.image.load('data/WindowIcon.png')
    pygame.display.set_icon(icon)

    # размеры окна:
    # noinspection PyUnboundLocalVariable
    size = width, height = 1000, 600
    # screen — холст, на котором нужно рисовать:
    screen = pygame.display.set_mode(size)

    FPS = 50
    tile_width = tile_height = 25
    power = 50

    small_font = pygame.font.SysFont('Menlo', 24)
    medium_font = pygame.font.SysFont('Menlo', 48)
    large_font = pygame.font.SysFont('Menlo', 72)

    block_image = load_image('ground.jpg')
    block_image = pygame.transform.scale(block_image,
                                         (tile_width, tile_height))
    empty_image = load_image('empty.png')
    empty_image = pygame.transform.scale(empty_image,
                                         (tile_width, tile_height))
    tile_images = {
        'wall': block_image,
        'empty': empty_image
    }
    player_image = load_image('tank.png')
    player_image = pygame.transform.scale(player_image, (80, 45))

    enemy_image = load_image('tank.png')
    enemy_image = pygame.transform.scale(enemy_image, (80, 45))
    enemy_image = pygame.transform.flip(enemy_image, True, False)

    bomb_image = load_image('bomb.png')
    bomb_image = pygame.transform.scale(bomb_image, (10, 10))

    background_image = pygame.image.load('data/background.jpg').convert()
    background_image = pygame.transform.scale(background_image,
                                              (width, height))

    fire_sound = pygame.mixer.Sound('data/shoot_sound.mp3')

    # основной персонаж
    player = None

    # группы спрайтов
    sprite_group = SpriteGroup()
    block_group = SpriteGroup()
    hero_group = SpriteGroup()
    enemy_group = SpriteGroup()
    bullet_group = SpriteGroup()

    clock = pygame.time.Clock()

    start_screen()

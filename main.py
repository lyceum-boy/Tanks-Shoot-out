#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Creates Tanks game.

It just realises a game with tanks in Python using PyGame module.
Functions description:
1) ;
N) .
"""

import os
import random
import sqlite3
import time

import pygame

__author__ = ["Ilya B. Anosov", "Sofia P. Kalinina"]
__credits__ = ["Georgiy A. Darovskih"]
__version__ = "1.0.1"
__maintainer__ = ["Ilya B. Anosov"]
__email__ = "anosovilya465@yandex.ru"
__status__ = "Development"


def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname).convert()
        image = pygame.transform.scale(image, (80, 40))
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)

    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


if __name__ == '__main__':
    # инициализация Pygame:
    pygame.init()
    # размеры окна:
    size = width, height = 800, 600
    # screen — холст, на котором нужно рисовать:
    screen = pygame.display.set_mode(size)
    # формирование кадра:
    # команды рисования на холсте
    # ...
    # ...
    # смена (отрисовка) кадра:
    pygame.display.flip()
    # ожидание закрытия окна:
    while pygame.event.wait().type != pygame.QUIT:
        pass
    # завершение работы:
    pygame.quit()

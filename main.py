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
import sys

import pygame

__author__ = ["Ilya B. Anosov", "Sofia P. Kalinina"]
__credits__ = ["Georgiy A. Darovskih"]
__version__ = "1.0.1"
__maintainer__ = ["Ilya B. Anosov"]
__email__ = "anosovilya465@yandex.ru"
__status__ = "Development"

BACKGROUND_POSITION = (0, 0)


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    sys.excepthook = except_hook

    # инициализация Pygame:
    pygame.init()

    # размеры окна:
    size = width, height = 800, 600

    # screen — холст, на котором нужно рисовать:
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption('Tanks. Shoot-out')
    icon = pygame.image.load('data/WindowIcon.png')
    pygame.display.set_icon(icon)

    background_image = pygame.image.load("data/BackgroundImage.jpg").convert()
    background_image = pygame.transform.scale(background_image, size)
    screen.blit(background_image, BACKGROUND_POSITION)

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

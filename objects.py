from setings import *
from random import randint
import pygame as pg
from loguru import logger


class RND:
    @staticmethod
    def create_rnd(a: int, b: int, n: int):
        rnd_list = list()
        for _ in range(n):
            rnd_list.append(randint(a, b))
        return rnd_list


class ObjGame(pg.Rect):
    def __init__(self, size_rect: tuple, pos: tuple = None):
        if pos is None:
            pos = (randint(0, width_window * 10), randint(0, height_window * 10))
        super().__init__(*pos, size_rect[0], size_rect[1])
        self._surf = pg.Surface(size_rect)
        self._surf.fill((200, 200, 200))
        self.color = RND.create_rnd(0, 150, 4)
        pg.draw.circle(self._surf, self.color, (size_rect[0] // 2, size_rect[1] // 2), size_rect[0] // 2)

    def surf(self):
        return self._surf


class Player(ObjGame):
    def __init__(self, size_rect: tuple = (10, 10)):
        super().__init__(size_rect=size_rect, pos=(width_window//2, height_window//2))
        self.__eaten = 0
        self.__size = 10

    def eating(self):
        self.__eaten += 1
        if self.__size < 100:
            self.__resize()
        logger.debug((self.__eaten, self.__size))
        logger.debug((self.topleft, self.bottomright))

    def __resize(self):
        self.__size += 2
        self._surf = pg.transform.scale(self._surf, (self.__size, self.__size))
        self._surf.fill((200, 200, 200))
        self.w += 2
        self.h += 2
        self.x -= 1
        self.y -= 1
        pg.draw.circle(self._surf, self.color, (self.__size // 2, self.__size // 2), self.__size // 2)

    def size(self):
        return self.__size

    @staticmethod
    def move_player(keys, eats):
        actions = {
            'up': (0, step_player),
            'down': (0, -step_player),
            'right': (-step_player, 0),
            'left': (step_player, 0)
        }

        if keys[pg.K_w]:
            eats.move_eats(actions['up'])
        if keys[pg.K_s]:
            eats.move_eats(actions['down'])
        if keys[pg.K_d]:
            eats.move_eats(actions['right'])
        if keys[pg.K_a]:
            eats.move_eats(actions['left'])


class Eat(ObjGame):
    def __init__(self, size_rect: tuple):
        super().__init__(size_rect=size_rect)

    def get_center(self):
        return self.center


class Eats:
    __EATS = dict()

    def __init__(self, quantity: int, size_rect: tuple = (5, 5)):
        self.size_rect = size_rect
        self.add_eats(quantity)

    def add_eats(self, quantity: int):
        for _ in range(quantity):
            eat = Eat(self.size_rect)
            self.__EATS[eat.get_center()] = eat

    def get_eats(self):
        return self.__EATS

    def del_eat(self, center_eats: list):
        for eat in center_eats:
            del self.__EATS[eat]
        self.add_eats(len(center_eats))

    def move_eats(self, cord: tuple):
        for eat in self.__EATS.values():
            eat.move_ip(*cord)

        for eat_center, eat in self.__EATS.copy().items():
            del self.__EATS[eat_center]
            eat_center = (eat_center[0] + cord[0], eat_center[1] + cord[1])
            self.__EATS[eat_center] = eat

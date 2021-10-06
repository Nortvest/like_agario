from setings import *
from random import randint
import pygame as pg


class RND:
    @staticmethod
    def create_rnd(a: int, b: int, n: int):
        rnd_list = list()
        for _ in range(n):
            rnd_list.append(randint(a, b))
        return rnd_list


class Property:
    def __set_name__(self, owner, name):
        self.__name = name

    def __set__(self, instance, value):
        instance.__dict__[self.__name] = value

    def __get__(self, instance, owner):
        return instance.__dict__[self.__name]


class ObjGame(pg.Rect):
    def __init__(self, size_rect: tuple):
        super().__init__((randint(0, width_window), randint(0, height_window), size_rect[0], size_rect[1]))
        self._surf = pg.Surface(size_rect)
        self._surf.fill((200, 200, 200))
        self.color = RND.create_rnd(0, 150, 4)
        pg.draw.circle(self._surf, self.color, (size_rect[0] // 2, size_rect[1] // 2), size_rect[0] // 2)

    def surf(self):
        return self._surf


class Player(ObjGame):
    site = Property()

    def __init__(self, size_rect: tuple = (10, 10)):
        super().__init__(size_rect=size_rect)
        self.__eaten = 0
        self.__size = 10

    def eating(self):
        self.__eaten += 1
        if not self.__eaten % 10 and self.__size < 100:
            self.__resize()

    def __resize(self):
        self.__size += 1
        self._surf = pg.transform.scale(self._surf, (self.__size, self.__size))
        self._surf.fill((200, 200, 200))
        self.w += 1
        self.h += 1
        pg.draw.circle(self._surf, self.color, (self.__size // 2, self.__size // 2), self.__size // 2)

    def size(self):
        return self.__size

    def move(self, keys, **kwargs):
        actions = {
            'up': (0, -step_player),
            'down': (0, step_player),
            'right': (step_player, 0),
            'left': (-step_player, 0)
        }

        if keys[pg.K_w] and self.y > 0:
            self.move_ip(actions['up'])
        if keys[pg.K_s] and self.y + self.h < height_window:
            self.move_ip(actions['down'])
        if keys[pg.K_d] and self.x + self.w < width_window:
            self.move_ip(actions['right'])
        if keys[pg.K_a] and self.x > 0:
            self.move_ip(actions['left'])


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

from objects import *
import sys


class Game:
    def __init__(self):
        pg.init()
        self.clock = pg.time.Clock()
        self.display = pg.display.set_mode((width_window, height_window))
        self.player = Player()
        self.eats = Eats(quantity_eats)

    @staticmethod
    def execute_event():
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()

    def blit_eats(self):
        delete_eat = list()
        for eat_center, eat_obj in self.eats.get_eats().items():
            if self.player.collidepoint(eat_center):
                delete_eat.append(eat_center)
                self.player.eating()
            self.display.blit(eat_obj.surf(), eat_obj)
        self.eats.del_eat(delete_eat)

    def start_game(self):
        while True:
            self.execute_event()
            self.display.fill((200, 200, 200))

            self.blit_eats()

            self.display.blit(self.player.surf(), self.player)
            keys = pg.key.get_pressed()
            self.player.move(keys)

            pg.display.update()
            self.clock.tick(60)


if __name__ == '__main__':
    game = Game()
    game.start_game()
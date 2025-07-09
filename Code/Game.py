import pygame

from Code.Const import WIN_WIDTH, WIN_HEIGHT, MENU_OPTION
from Code.City import City
from Code.Menu import Menu


class Game:

    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode(size=(WIN_WIDTH, WIN_HEIGHT))

    def run(self):
        while True:
            menu = Menu(self.window)
            menu_return = menu.run()


            if menu_return in MENU_OPTION[0]:
                city = City(self.window, 'City1')
                city_return = city.run()
            elif menu_return == MENU_OPTION[2]:
                pygame.quit()
                quit()
            else:
                pass


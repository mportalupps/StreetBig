import pygame

from Code.Const import WIN_WIDTH, WIN_HEIGHT, MENU_OPTION
from Code.City import City
from Code.Menu import Menu


class Game:

    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode(size=(WIN_WIDTH, WIN_HEIGHT))
        self.city_index = 0  # Começa na primeira cidade
        self.city_names = ['City1', 'City2', 'City3']

    def run(self):
        while True:
            menu = Menu(self.window)
            menu_return = menu.run()

            if menu_return in MENU_OPTION[0]:
                self.run_city_loop()
            elif menu_return == MENU_OPTION[2]:
                pygame.quit()
                quit()
            else:
                pass

    def run_city_loop(self):
        while True:
            city_name = self.city_names[self.city_index % len(self.city_names)]
            city = City(self.window, city_name)
            city_return = city.run()
            if city_return == "menu":
                break

            # Avança para a próxima cidade
            self.city_index += 1

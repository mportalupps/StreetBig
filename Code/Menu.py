import pygame.image
from pygame import Surface, Rect
from pygame.font import Font

from Code.Const import WIN_WIDTH, MENU_OPTION


class Menu:

    def __init__(self, window):
        self.window = window
        self.surf = pygame.image.load('./asset/Menu.png')
        self.rect = self.surf.get_rect(left=0, top=0)

    def run(self, ):
        pygame.mixer_music.load('./asset/MenuSound.mp3')
        pygame.mixer_music.play(-1)
        while True:
            self.window.blit(source=self.surf, dest=self.rect)
            self.menu_text(55, "StreetBig", (255, 100, 0), ((WIN_WIDTH / 2), 145), sombra=True)

            for i in range(len(MENU_OPTION)):
                self.menu_text(25, MENU_OPTION[i], (255, 255, 255), ((WIN_WIDTH / 2), 172 + 22 * i), sombra=True)

            pygame.display.flip()

        # Check for all events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                   pygame.quit() # Close Window
                   quit() # End pygame

    def menu_text(self, text_size: int, text: str, text_color: tuple, text_center_pos: tuple, sombra: bool = False):
        text_font: Font = pygame.font.SysFont(name="Lucida Sans Typewriter", size=text_size, bold=True)
        text_surf: Surface = text_font.render(text, True, text_color).convert_alpha()
        text_rect: Rect = text_surf.get_rect(center=text_center_pos)

        if sombra:
            sombra_color = (0, 0, 0)  # cor da sombra: preto
            sombra_offset = (2, 2)  # deslocamento da sombra
            sombra_surf = text_font.render(text, True, sombra_color).convert_alpha()
            sombra_rect: Rect = sombra_surf.get_rect(center=(text_center_pos[0] + sombra_offset[0],
                                                             text_center_pos[1] + sombra_offset[1]))
            self.window.blit(source=sombra_surf, dest=sombra_rect)

        self.window.blit(source=text_surf, dest=text_rect)
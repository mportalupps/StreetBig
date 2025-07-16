import sys
import random
import pygame
from pygame import Surface, Rect
from pygame.font import Font

from Code.Const import WIN_HEIGHT
from Code.Entity import Entity
from Code.EntityFactory import EntityFactory


class City:

    def __init__(self, window, name):
        self.window = window
        self.name = name
        self.entity_list: list[Entity] = []
        self.entity_list.extend(EntityFactory.get_entity('City1Bg'))
        self.entity_list.append(EntityFactory.get_entity('Runner'))

        # Configurações spawn inimigos
        self.enemy_types = ['DogBlack', 'DogWhite', 'CatOrange', 'CatBlue', 'RatBrown', 'RatBlue']
        self.min_distance_between_enemies = 400  # distância mínima em pixels entre inimigos
        self.spawn_cooldown = 1500  # tempo mínimo entre spawns em ms
        self.last_spawn_time = 0

        self.timeout = 20000
        self.speed_multiplier = 1.0
        self.difficulty_timer = 0

        # Spawna alguns inimigos iniciais
        for enemy_name in self.enemy_types:
            self.add_enemies(enemy_name, 1)

    def add_enemies(self, name: str, quantity: int):
        for _ in range(quantity):
            position = (random.randint(2000, 20000), 400)
            self.entity_list.append(EntityFactory.get_entity(name, position))

    def can_spawn_enemy_at(self, x_pos):
        # Verifica se a posição está suficientemente longe de todos os inimigos atuais
        enemies = [e for e in self.entity_list if hasattr(e, 'speed')]
        for e in enemies:
            if abs(e.rect.x - x_pos) < self.min_distance_between_enemies:
                return False
        return True

    def try_spawn_enemy(self):
        now = pygame.time.get_ticks()
        if now - self.last_spawn_time < self.spawn_cooldown:
            return

        for _ in range(10):
            enemy_name = random.choice(self.enemy_types)
            pos_x = random.randint(2000, 20000)
            pos_y = 400

            if self.can_spawn_enemy_at(pos_x):
                self.entity_list.append(EntityFactory.get_entity(enemy_name, (pos_x, pos_y)))
                self.last_spawn_time = now
                break

    def run(self):
        pygame.mixer_music.load(f'./asset/{self.name}.mp3')
        pygame.mixer_music.play(-1)
        clock = pygame.time.Clock()
        while True:
            clock.tick(60)
            for ent in self.entity_list:
                self.window.blit(source=ent.surf, dest=ent.rect)
                ent.move()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.city_text(14, f'{self.name} - Timeout:{self.timeout / 1000 :.1f}s', (255, 255, 255), (10, 5))
            self.city_text(14, f'fps: {clock.get_fps() :.0f}', (255, 255, 255), (10, WIN_HEIGHT - 35))

            self.difficulty_timer += clock.get_time()
            if self.difficulty_timer >= 10000:
                self.difficulty_timer = 0
                self.speed_multiplier += 0.1

            # Atualiza velocidade dos inimigos e outros que suportem
            for ent in self.entity_list:
                if hasattr(ent, 'set_speed_multiplier'):
                    ent.set_speed_multiplier(self.speed_multiplier)

            # Tenta spawnar inimigos espaçados
            self.try_spawn_enemy()

            pygame.display.flip()

    def city_text(self, text_size: int, text: str, text_color: tuple, text_pos: tuple):
        text_font: Font = pygame.font.SysFont(name="Lucida Sans TyperWriter", size=text_size)
        text_surf: Surface = text_font.render(text, True, text_color).convert_alpha()
        text_rect: Rect = text_surf.get_rect(left=text_pos[0], top=text_pos[1])
        self.window.blit(source=text_surf, dest=text_rect)

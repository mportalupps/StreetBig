import sys
import random
import pygame
from pygame import Surface, Rect
from pygame.font import Font

from Code.Const import WIN_HEIGHT
from Code.Enemy import Enemy
from Code.Entity import Entity
from Code.EntityFactory import EntityFactory


class City:

    def __init__(self, window, name):
        self.window = window
        self.name = name
        self.entity_list: list[Entity] = []
        self.entity_list.extend(EntityFactory.get_entity('City1Bg'))
        self.runner = EntityFactory.get_entity('Runner')
        self.entity_list.append(self.runner)

        self.score = 0
        self.score_timer = 0.0
        self.font = pygame.font.SysFont("Lucida Sans TyperWriter", 36)

        self.game_over = False

        # Configurações spawn inimigos
        self.enemy_types = ['DogBlack', 'DogWhite', 'CatOrange', 'CatBlue', 'RatBrown', 'RatBlue']
        self.min_distance_between_enemies = 400  # distância mínima em pixels entre inimigos
        self.spawn_cooldown = 1500  # tempo mínimo entre spawns em ms
        self.last_spawn_time = 0



        self.timeout = 20000
        self.speed_multiplier = 1.0
        self.difficulty_timer = 0

        for enemy_name in self.enemy_types:
            self.add_enemies(enemy_name, 2)

    def update_score(self, dt):
        self.score_timer += dt

        if self.score_timer >= 0.1:
            self.score += 1
            self.score_timer -= 0.1

    def draw_game_over(self):
        font = pygame.font.SysFont("Lucida Sans TyperWriter", 48)
        text = font.render("Você perdeu!", True, (255, 50, 50))
        rect = text.get_rect(center=(self.window.get_width() // 2, self.window.get_height() // 2 - 50))
        self.window.blit(text, rect)

        # Botão de reinício
        button_font = pygame.font.SysFont("Lucida Sans TyperWriter", 32)
        button_text = button_font.render("Voltar", True, (255, 255, 255))
        self.restart_button_rect = button_text.get_rect(
            center=(self.window.get_width() // 2, self.window.get_height() // 2 + 30))
        pygame.draw.rect(self.window, (50, 50, 50), self.restart_button_rect.inflate(20, 10))
        self.window.blit(button_text, self.restart_button_rect)

    def add_enemies(self, name: str, quantity: int):
        for _ in range(quantity):
            position = (random.randint(2000, 20000), 400)
            self.entity_list.append(EntityFactory.get_entity(name, position))

    def can_spawn_enemy_at(self, x_pos):
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
        self.restart_button_rect = pygame.Rect(0, 0, 0, 0)

        while True:
            dt = clock.tick(60) / 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if self.game_over and event.type == pygame.MOUSEBUTTONDOWN:
                    if self.restart_button_rect.collidepoint(event.pos):
                        return
                if self.game_over and event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        return

            if not self.game_over:
                self.update_score(dt)

                self.window.fill((0, 0, 0))

                for ent in self.entity_list:
                    self.window.blit(ent.surf, ent.rect)
                    ent.move()

                # Colisão e game over
                for ent in self.entity_list:
                    if isinstance(ent, Enemy):
                        offset_x = ent.rect.left - self.runner.rect.left
                        offset_y = ent.rect.top - self.runner.rect.top
                        if self.runner.mask.overlap(ent.mask, (offset_x, offset_y)):
                            self.game_over = True
                            pygame.mixer_music.pause()
                            self.save_high_score()
                            break

                self.city_text(20, f'{self.score:06d}', (255, 255, 255), (10, 10))
                self.city_text(16, f'fps: {clock.get_fps() :.0f}', (255, 255, 255), (10, WIN_HEIGHT - 35))

                self.difficulty_timer += clock.get_time()
                if self.difficulty_timer >= 10000:
                    self.difficulty_timer = 0
                    self.speed_multiplier += 0.1

                for ent in self.entity_list:
                    if hasattr(ent, 'set_speed_multiplier'):
                        ent.set_speed_multiplier(self.speed_multiplier)

                self.try_spawn_enemy()

            else:
                self.draw_game_over()

            pygame.display.flip()

    def city_text(self, text_size: int, text: str, text_color: tuple, text_pos: tuple):
        text_font: Font = pygame.font.SysFont(name="Lucida Sans TyperWriter", size=text_size)
        text_surf: Surface = text_font.render(text, True, text_color).convert_alpha()
        text_rect: Rect = text_surf.get_rect(left=text_pos[0], top=text_pos[1])
        self.window.blit(source=text_surf, dest=text_rect)

    def save_high_score(self):  # salva os 3 maiores scores
        score_file = 'score.txt'
        try:
            with open(score_file, 'r') as file:  # tenta abrir o arquivo
                scores = [int(line.strip()) for line in file.readlines()]
        except FileNotFoundError:
            scores = []

        scores.append(self.score)  # adiciona score atual
        scores = sorted(scores, reverse=True)[:3]  # mantém só os 3 maiores

        with open(score_file, 'w') as file:  # sobrescreve com os 3 maiores
            for s in scores:
                file.write(f"{s}\n")

        self.top_scores = scores

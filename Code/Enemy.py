import pygame
import random

from Code.Const import FRAME_COUNTS
from Code.Entity import Entity

class Enemy(Entity):
    def __init__(self, name: str, position: tuple):
        super().__init__(name + '0', position)

        frame_count = FRAME_COUNTS.get(name, 6)

        self.frames = [
            pygame.transform.scale(
                pygame.image.load(f'./asset/{name}{i}.png').convert_alpha(),
                (110, 110)
            )
            for i in range(frame_count)
        ]

        self.current_frame = 0
        self.frame_accumulator = 0.0
        self.animation_speed = 0.2
        self.speed_multiplier = 1

        self.surf = self.frames[self.current_frame]
        self.rect = self.surf.get_rect(topleft=position)

        self.speed = 7 # velocidade de corrida para esquerda

        self.respawn_delay = 0
        self.waiting = False

    def move(self):
        if self.waiting:
            self.respawn_delay -= 1
            if self.respawn_delay <= 0:
                # Reaparece fora da tela, com posição e tempo aleatórios
                self.rect.left = random.randint(850, 1200)
                self.rect.top = 300
                self.waiting = False
            return

        self.rect.x -= self.speed * self.speed_multiplier  # Velocidade para esquerda

        # Animação
        self.frame_accumulator += self.animation_speed
        if self.frame_accumulator >= 1:
            self.frame_accumulator = 0
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.surf = self.frames[self.current_frame]

        # Se sair da tela, volta para a direita em posição aleatória
        if self.rect.right < 0:
            nova_x = random.randint(2000, 20000)
            self.rect.left = nova_x

    def set_speed_multiplier(self, value: float):
        self.speed_multiplier = value

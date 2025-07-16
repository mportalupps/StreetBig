import pygame
from Code.Entity import Entity

class Runner(Entity):
    def __init__(self, name: str, position: tuple):
        super().__init__(name + '0', position)

        # carregar todos os frames numa lista
        self.frames_run = [
            pygame.transform.scale(
                pygame.image.load(f'./asset/{name}{i}.png').convert_alpha(),
                (225, 225)
            )
            for i in range(10)
        ]

        self.frames_jump = self.frames_run

        self.current_frame = 0
        self.animation_speed = 0.15  # controla a velocidade da animação (frames por atualização)
        self.frame_accumulator = 0.0

        self.state = 'run'
        self.vel_y = 0
        self.gravity = 1
        self.jump_force = -25
        self.on_ground = True

        # usar a imagem inicial e retângulo dela
        self.surf = self.frames_run[self.current_frame]
        self.rect = self.surf.get_rect(topleft=position)

        self.chao_y = self.rect.y + self.surf.get_height()

    def update(self, ):
        pass

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE] and self.on_ground:
            self.vel_y = self.jump_force
            self.on_ground = False
            self.state = 'jump'

        if keys[pygame.K_DOWN] and not self.on_ground:
            self.vel_y += self.gravity * 2.5

        self.vel_y += self.gravity
        self.rect.y += self.vel_y

        pe_do_personagem = self.rect.y + self.surf.get_height()

        if pe_do_personagem >= self.chao_y:
            self.rect.y = self.chao_y - self.surf.get_height()
            self.vel_y = 0
            self.on_ground = True
            self.state = 'run'

        frames = self.frames_run if self.state == 'run' else self.frames_jump

        # Animação
        self.frame_accumulator += self.animation_speed
        if self.frame_accumulator >= 1:
            self.frame_accumulator = 0
            self.current_frame = (self.current_frame + 1) % len(frames)
            self.surf = frames[self.current_frame]
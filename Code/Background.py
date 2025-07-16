from Code.Const import WIN_WIDTH, ENTITY_SPEED
from Code.Entity import Entity

class Background(Entity):

    def __init__(self, name: str, position: tuple):
        super().__init__(name, position)
        self.speed_multiplier = 1

    def move(self):
        self.rect.centerx -= ENTITY_SPEED[self.name] * self.speed_multiplier
        if self.rect.right <= 0:
            self.rect.left = WIN_WIDTH

    def set_speed_multiplier(self, value: float):
        self.speed_multiplier = value
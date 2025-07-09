from Code.Const import WIN_WIDTH
from Code.Entity import Entity

class Background(Entity):

    def __init__(selfself, name: str, position: tuple):
        super().__init__(name, position)

    def move(self, ):
        self.rect.centerx -= 3
        if self.rect.right <= 0:
            self.rect.left = WIN_WIDTH
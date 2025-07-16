from Code.Background import Background
from Code.Const import WIN_WIDTH
from Code.Runner import Runner
from Code.Enemy import Enemy


class EntityFactory:

    @staticmethod
    def get_entity(entity_name: str, position=(0,0)):
        match entity_name:
            case 'City1Bg':
                list_bg = []
                for i in range(7):
                    list_bg.append(Background(f'City1Bg{i}', (0, 0)))
                    list_bg.append(Background(f'City1Bg{i}', (WIN_WIDTH, 0)))
                return list_bg
            case 'Runner':
                return Runner('Runner', (30, 300))
            case 'DogBlack':
                return Enemy('DogBlack', position)
            case 'DogWhite':
                return Enemy('DogWhite', position)
            case 'CatOrange':
                return Enemy('CatOrange', position)
            case 'CatBlue':
                return Enemy('CatBlue', position)
            case 'RatBrown':
                return Enemy('RatBrown', position)
            case 'RatBlue':
                return Enemy('RatBlue', position)
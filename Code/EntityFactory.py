from Code.Background import Background
from Code.Const import WIN_WIDTH
from Code.Runner import Runner
from Code.Enemy import Enemy


class EntityFactory:

    @staticmethod
    def get_entity(entity_name: str, position=(0, 0)):
        match entity_name:
            case 'City1Bg':
                return EntityFactory._load_backgrounds('City1Bg', 7)
            case 'City2Bg':
                return EntityFactory._load_backgrounds('City2Bg', 6)
            case 'City3Bg':
                return EntityFactory._load_backgrounds('City3Bg', 6)
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

    @staticmethod
    def _load_backgrounds(prefix: str, count: int):
        bg_list = []
        for i in range(count):
            bg_list.append(Background(f'{prefix}{i}', (0, 0)))
            bg_list.append(Background(f'{prefix}{i}', (WIN_WIDTH, 0)))
        return bg_list

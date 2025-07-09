from enum import nonmember

import pygame

from Code.Entity import Entity
from Code.EntityFactory import EntityFactory


class City:

    def __init__(self, window, name):
        self.window = window
        self.name = name
        self.entity_list: list[Entity] = []
        self.entity_list.extend(EntityFactory.get_entity('City1Bg'))

    def run(self):
        while True:
            for ent in self.entity_list:
                self.window.blit(source=ent.surf, dest=ent.rect)
                ent.move()
            pygame.display.flip()
        pass
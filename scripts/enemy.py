import pygame
from settings import *
from misc import *


class enemy(pygame.sprite.Sprite):
    def __init__(self, players, position, group, type = 'zombie'):
        super().__init__(group)
        self.zIndex = layers["main"]
        self.image = pygame.image.load('sprites/enemies/'+ type + '.png')
        self.rect = self.image.get_rect(center = (position[0]*tileSize, position[1]*tileSize))
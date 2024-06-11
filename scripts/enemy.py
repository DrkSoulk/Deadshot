import pygame
from settings import *
from misc import *

wallweightmult = 1

class enemy(pygame.sprite.Sprite):
    def __init__(self, players, startposition, group, collisions, type = 'zombie'):
        super().__init__(group)
        self.zIndex = layers["main"]
        self.image = pygame.image.load('sprites/enemies/'+ type + '.png')
        self.rect = self.image.get_rect(center = (startposition[0]*tileSize, startposition[1]*tileSize))
        self.players = players
        self.position = pygame.math.Vector2(self.rect.center)
        self.speed = 0.5
        self.collisions = collisions

    def move(self):
        self.target = self.players[0]

        # Finds closest player
        for player in self.players:
            xdiff = abs(self.position.x - player.position.x)
            ydiff = abs(self.position.y - player.position.y)
            if  xdiff + ydiff < (abs(self.position.x - self.target.position.x)
                                 + abs(self.position.y - self.target.position.y)):
                self.target = player
        weight = pygame.math.Vector2((0,0))
        xplayerweight = (self.target.position.x - self.position.x)/tileSize
        yplayerweight = (self.target.position.y - self.position.y)/tileSize
        weightdenom = abs(yplayerweight) + abs(xplayerweight)
        weight.x = xplayerweight/weightdenom
        weight.y = yplayerweight/weightdenom

        self.position.x += self.speed*(weight.x)
        self.position.y += self.speed*(weight.y)
    def update(self, deltatime):
        self.move()
        self.rect.center = self.position
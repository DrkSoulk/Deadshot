import pygame
from settings import *
from misc import *
from enemydata import enemydata

class enemy(pygame.sprite.Sprite):
    def __init__(self, players, startposition, \
                 group, collisions, type = 'zombie'):
        super().__init__(group)
        self.zIndex = layers["main"]
        self.image = pygame.image.load('sprites/enemies/'+ type + '.png')
        self.rect = self.image.get_rect(center = (startposition[0]*tileSize,\
                                                   startposition[1]*tileSize))
        self.players = players
        self.position = pygame.math.Vector2(self.rect.center)
        self.speed = enemydata[type]['speed']
        self.collisions = collisions
        self.hitbox = self.rect.copy()
        self.health = enemydata[type]['health']
        self.type = type

        
    def move(self):
        '''
        Moves enemy towards nearest player, checking for collisions.
        '''
        self.target = self.players[0]

        # Finds closest player (only relevant in theoretical multiplayer)
        for player in self.players:
            xdiff = abs(self.position.x - player.position.x)
            ydiff = abs(self.position.y - player.position.y)
            if  xdiff+ydiff < (abs(self.position.x - self.target.position.x)+
                               abs(self.position.y - self.target.position.y)):
                self.target = player
        
        # Get x/y ratios of player position relative to self position
        weight = pygame.math.Vector2((0,0))
        xplayerweight = (self.target.position.x - self.position.x)/tileSize
        yplayerweight = (self.target.position.y - self.position.y)/tileSize
        weightdenom = abs(yplayerweight) + abs(xplayerweight)
        if weightdenom == 0:
            weightdenom = 1
        weight.x = xplayerweight/weightdenom
        weight.y = yplayerweight/weightdenom

        # Move x with proper ratio of total speed, if not colliding
        self.position.x += self.speed*(weight.x)
        for i in self.collisions:
            self.hitbox.centerx = self.position.x
            if hasattr(i, "hitbox") and i.hitbox.colliderect(self.hitbox):
                self.position.x -= self.speed*(weight.x)

        # Move x with proper ratio of total speed, if not colliding
        self.position.y += self.speed*(weight.y)
        for i in self.collisions:
            self.hitbox.centery = self.position.y
            if hasattr(i, "hitbox") and i.hitbox.colliderect(self.hitbox):
                self.position.y -= self.speed*(weight.y)
        


    def update(self, deltatime):
        # Update position
        self.move()
        self.rect.center = self.position

        # Change speed relative to remaining health
        self.speed = enemydata[self.type]['speed']\
            *(self.health/enemydata[self.type]['health'])
        
        # Check for death
        if self.health <= 0:
            self.kill()
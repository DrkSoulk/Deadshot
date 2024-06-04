import pygame
from settings import *
from os import walk

# Sprite groups
projectiles = pygame.sprite.Group()
vfx = pygame.sprite.Group()

class timer:
    def __init__(self, target):
        # Timer setup
        self.target = target
        self.time = target
        self.active = False
    
    def start(self):
        self.time = self.target
        self.active = True
    
    def update(self, deltaTime):
        if self.active:
            self.time -= deltaTime

            if self.time <= 0:
                self.time = 0
                self.active = False

def importSpriteSheets(path):
    spriteSheets = {}

    # Loop through spritesheets
    for _, _, i in walk(path):
        for v in i:
            spriteSheets[v[:-4]] = pygame.image.load(path + "/" + v).convert_alpha()
    
    return spriteSheets

def importSounds(path):
    sounds = {}

    # Loop through sounds
    for _, _, i in walk(path):
        for v in i:
            sounds[v[:-4]] = pygame.mixer.Sound(path + "/" + v)
    
    return sounds

def scaleImage(image, factor):
    return pygame.transform.scale(image, (image.get_width() * factor, image.get_height() * factor))
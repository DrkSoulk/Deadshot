'''
This module contains a bunch of constants and config information
'''

import pygame

# Game resolution
resolution = pygame.math.Vector2(960, 640)
middleScreen = pygame.math.Vector2(resolution.x // 2, resolution.y // 2)

# Overlay settings
overlayOffset = pygame.math.Vector2(30)
fontSize = 24

# Map settings
tileSize = 18
scaleFactor = 2.5
maxLookDistance = pygame.math.Vector2(150)

# Misc style settings
menuBGcolour = (50,20,20)
selectorColour = (180,0,0)

# Player keybinds
keybinds = {
    "left": pygame.K_a,
    "right": pygame.K_d,
    "up": pygame.K_w,
    "down": pygame.K_s,
    "roll": pygame.K_LSHIFT,
    "primary": pygame.K_1,
    "secondary": pygame.K_2,
    "swap": pygame.K_q,
    "reload": pygame.K_r,
    "endGame": pygame.K_ESCAPE,
    "pause": pygame.K_p,
    "select": pygame.K_RETURN,
    "menuUp": pygame.K_UP,
    "menuDown": pygame.K_DOWN
}

# Drawing layers
layers = {
    "floor": 0,
    "projectiles": 1,
    "main": 2,
    "objects": 3,
    "vfx": 4
}

# Sound mixer
mixer = {
    "master": 1,
    "player": 0.6,
    "guns": 0.4
}

# Map List
maplist = [
    'test',
    'sewer',
    'rock',
    'back'
]
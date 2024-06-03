import pygame

# Game resolution
resolution = pygame.math.Vector2(960, 640)
middleScreen = pygame.math.Vector2(resolution.x // 2, resolution.y // 2)

# Overlay settings
overlayOffset = pygame.math.Vector2(30)
fontSize = 24

# Map settings
tileSize = 32
maxLookDistance = pygame.math.Vector2(150)

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
    "endGame": pygame.K_ESCAPE
}

# Drawing layers
layers = {
    "floor": 0,
    "projectiles": 1,
    "main": 2,
    "vfx": 3
}

# Sound mixer
mixer = {
    "master": 1,
    "sfx": {
        "master": 0.8,
        "player": 0.2,
        "guns": 0.4
    }
}
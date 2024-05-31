import pygame
import pygame.freetype
from settings import *

class overlay(pygame.sprite.Sprite):
    def __init__(self):
        # Overlay setup
        self.overlay = pygame.surface.Surface(resolution - overlayOffset, pygame.SRCALPHA, 32).convert_alpha()
        self.rect = self.overlay.get_rect(center = middleScreen)
        
        # Import font
        self.basicFont = pygame.freetype.Font("fonts/basic.ttf", fontSize)
    
    def update(self, player):
        # Clear overlay
        self.overlay.fill((0, 0, 0, 0))

        # Get overlay size
        size = pygame.math.Vector2(self.overlay.get_size())
        
        # Draw ammo display
        if player.currentItem.type == "guns":
            string = str(player.currentItem.clip) + " l " + str(player.inventory["ammo"][player.currentItem.data["type"]])
            textSize = self.basicFont.get_rect(string)
            
            self.basicFont.render_to(self.overlay, (size.x - textSize.width, size.y - textSize.height), string, (255, 255, 255))
        
        # Return to be drawn
        return self.overlay, self.rect
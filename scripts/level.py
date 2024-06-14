import pygame
from settings import *
from misc import *
from player import player
from overlay import overlay
from pytmx.util_pygame import load_pygame
from enemy import enemy

class level:
    def __init__(self):
        # Get the screen
        self.screen = pygame.display.get_surface()

        # Sprite groups
        self.sprites = camera()
        self.map = pygame.sprite.Group()
        self.collisions = pygame.sprite.Group()

        # Drawing the player
        self.player = player((125, 125), self.sprites, self.collisions)

        # Drawing Enemies
        self.enemies = [enemy([self.player,], (10,10), self.sprites, self.collisions)]

        # Load map
        self.load(input("Choose a map (test, rock, sewer): "))
        
        # Drawing the overlay
        self.overlay = overlay()

    def load(self, map):
        # Remove map
        for i in self.sprites:
            for v in self.map:
                if i == v:
                    self.sprites.remove(i)
        
        # Reset map
        self.collisions.empty()
        self.map.empty()

        # Load map
        mapData = load_pygame("map/" + map + ".tmx")

        # Floor
        for x, y, image in mapData.get_layer_by_name("Floor").tiles():
            sprites((x * tileSize * scaleFactor, y * tileSize * scaleFactor), scaleImage(image, scaleFactor), self.map, layers["floor"])

        # Walls
        for x, y, image in mapData.get_layer_by_name("Walls").tiles():
            sprites((x * tileSize * scaleFactor, y * tileSize * scaleFactor), scaleImage(image, scaleFactor), [self.map, self.collisions])
        
        # Objects
        for i in mapData.get_layer_by_name("Objects"):
            sprites((i.x * scaleFactor, i.y * scaleFactor), scaleImage(i.image, scaleFactor), self.map, layers["objects"])
        
        # Add map to be drawn
        for i in self.map:
            self.sprites.add(i)

    def run(self, deltaTime):
        # Updating background
        self.screen.fill((0, 0, 0))

        # Adding projectiles
        for i in projectiles:
            i.collisions = self.collisions

            if i not in self.sprites:
                self.sprites.add(i)
        
        # Adding vfx
        for i in vfx:
            if i not in self.sprites:
                self.sprites.add(i)

        # Updating sprites
        self.sprites.drawSprites(self.player, self.enemies)
        self.sprites.update(deltaTime)
        
        # Updating overlay
        display, rect = self.overlay.update(self.player)
        self.screen.blit(display, rect)

class sprites(pygame.sprite.Sprite):
    def __init__(self, position, image, group, zIndex = layers["main"]):
        # Initialize the sprite
        super().__init__(group)

        # Sprite setup
        self.image = image
        self.rect = self.image.get_rect(topleft = position)
        self.hitbox = self.rect.copy()
        self.zIndex = zIndex

class camera(pygame.sprite.Group):
    def __init__(self):
        # Initialize the camera
        super().__init__()

        # Screen setup
        self.screen = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()
        self.goal = pygame.math.Vector2()

    def drawSprites(self, player, enemies):
        # Offset camera based on mouse position
        mouseOffset = middleScreen - pygame.mouse.get_pos()

        # Contrain mouse offset
        if mouseOffset.length() > maxLookDistance.length():
            constrainedOffset = mouseOffset.normalize() * maxLookDistance.length()
            mouseOffset = mouseOffset.lerp(constrainedOffset, 0.5)

        # Set the camera goal
        self.goal = player.rect.center - middleScreen - mouseOffset

        # Smoothen the camera
        self.offset.x = ((self.offset.x * 0.975) + (self.goal.x * 0.025))
        self.offset.y = ((self.offset.y * 0.975) + (self.goal.y * 0.025))

        # Draw sprites
        for i in layers.values():
            for v in self.sprites():
                if i == v.zIndex:
                    # Offset rect
                    newrect = v.rect.copy()
                    newrect.center -= self.offset

                    # Draw the player and player's current item
                    if v == player and player.currentItem != None:
                        player.updateOffset(self.offset)

                        if player.facingFront:
                            self.screen.blit(v.image, newrect)
                            self.screen.blit(player.currentItem.image, player.currentItem.rect)
                        else:
                            self.screen.blit(player.currentItem.image, player.currentItem.rect)
                            self.screen.blit(v.image, newrect)
                    if v in enemies:
                        self.screen.blit(v.image, newrect)
                    else:
                        self.screen.blit(v.image, newrect)
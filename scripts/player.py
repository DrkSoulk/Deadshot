'''
This module contains the player class.
This class is for the player controlled character.
'''

import pygame
from settings import *
from misc import *
from items import item

class player(pygame.sprite.Sprite):
    def __init__(self, position, group, collisions):
        # Initialize the player
        super().__init__(group)

        # Animation setup
        self.status = "idleFront"
        self.frame = 0
        self.flipped = False
        self.animations = {
            "idleFront": [4],
            "idleFrontSide": [4],
            "idleBack": [4],
            "idleBackSide": [4],
            "walkFront": [6],
            "walkFrontSide": [6],
            "walkBack": [6],
            "walkBackSide": [6]
        }

        # Get sprite sheets
        for i in self.animations.keys():
            for a, v in importSpriteSheets("sprites/player").items():
                if i == a:
                    self.animations[i].append(v)

        # Player setup
        self.image = pygame.Surface((tileSize, tileSize))
        self.rect = self.image.get_rect(center = position)
        
        self.zIndex = layers["main"]
        self.offset = pygame.math.Vector2()

        # Collision setup
        self.hitbox = self.rect.copy()
        self.collisions = collisions

        # Player stats
        self.speed = 200
        self.health = 100

        # Movement
        self.direction = pygame.math.Vector2()
        self.facingFront = True
        self.position = pygame.math.Vector2(self.rect.center)

        # Inventory setup
        self.inventory = {
            "primary": item("tommyGun", self.position),
            "secondary": item("pea", self.position),
            "ammo": {
                "nerfGun": 999,
                "pistol": 999,
                "smg": 999,
                "rifle": 999,
                "shotgun": 999,
                "sniper": 999,
                "guitar": 999,
                "letter": 999,
                "pea": 999,
                "revolver": 999,
                "tommyGun": 999,
                "tshirt": 999
            }
        }
        self.currentItem = self.inventory["primary"]
        self.currentItemIndex = "primary"
        
        # Button cooldown
        self.cooldown = timer(0.4)

        # Sound setup
        self.soundChannel = pygame.mixer.Channel(0)
        self.sounds = {
            "footsteps": {
                "ground": importSounds("sounds/player/footsteps/ground"),
                "carpet": importSounds("sounds/player/footsteps/carpet")
            },
            "items": importSounds("sounds/player/items")
        }

        # Set volume
        self.soundChannel.set_volume(mixer["player"])

        # Footstep setup
        self.footstepTimer = timer(0.4)
        self.footstepSound = "ground"
        self.footstepIndex = 0
    
    def animate(self, deltaTime):
        '''
        Cycles frames of animation
        '''
        # Change frame
        self.frame += 7 * deltaTime

        # Loop through frames
        if self.frame > self.animations[self.status][0]:
            self.frame = 0

        # Change image
        self.image = pygame.Surface.subsurface(
            self.animations[self.status][1], pygame.Rect(
                (tileSize * int(self.frame), 0), (tileSize, tileSize)))
        self.image = scaleImage(self.image, 2)
        self.rect = self.image.get_rect(center = self.position)

        # Flip if needed
        if self.flipped:
            self.image = pygame.transform.flip(self.image, 1, 0)
    
    def input(self, deltaTime):
        '''
        Gets and handles player input (Keyboard and mouse)
        '''
        # Getting every key pressed
        keys = pygame.key.get_pressed()

        # Get the mouse
        mouse = pygame.math.Vector2(pygame.mouse.get_pos())

        # Distance away from player
        mouseDistance = pygame.math.Vector2(maxLookDistance / 2).x

        # Type of animation
        animationType = "walk"

        # Offset position
        self.offsetPositon = self.position - self.offset

        # Reset player being flipped
        self.flipped = False

        # Horizontal movement
        if keys[keybinds["left"]]:
            self.direction.x = -1
        elif keys[keybinds["right"]]:
            self.direction.x = 1
        else:
            self.direction.x = 0
        
        # Vertical movement
        if keys[keybinds["up"]]:
            self.direction.y = -1
        elif keys[keybinds["down"]]:
            self.direction.y = 1
        else:
            self.direction.y = 0

        if self.direction == pygame.math.Vector2():
            animationType = "idle"
        
        if mouse.y >= self.offsetPositon.y:
            if mouse.x >= self.offsetPositon.x + mouseDistance:
                self.status = animationType + "FrontSide"
            elif mouse.x <= self.offsetPositon.x - mouseDistance:
                self.status = animationType + "FrontSide"
                self.flipped = True
            else:
                self.status = animationType + "Front"
            
            self.facingFront = True
        elif mouse.y <= self.offsetPositon.y - 1:
            if mouse.x >= self.offsetPositon.x + mouseDistance:
                self.status = animationType + "BackSide"
            elif mouse.x <= self.offsetPositon.x - mouseDistance:
                self.status = animationType + "BackSide"
                self.flipped = True
            else:
                self.status = animationType + "Back"
            
            self.facingFront = False
        else:
            self.status = animationType + "Front"
            self.facingFront = True
        
        # Swap item and reload
        if not self.cooldown.active:
            if keys[keybinds["primary"]]:
                self.currentItem = self.inventory["primary"]
                self.currentItemIndex = "primary"
                self.cooldown.start()
                self.soundChannel.play(self.sounds["items"]["swap"])
            elif keys[keybinds["secondary"]]:
                self.currentItem = self.inventory["secondary"]
                self.currentItemIndex = "secondary"
                self.cooldown.start()
                self.soundChannel.play(self.sounds["items"]["swap"])
            elif keys[keybinds["swap"]]:
                self.cooldown.start()
                self.soundChannel.play(self.sounds["items"]["swap"])

                if self.currentItemIndex == "primary":
                    self.currentItem = self.inventory["secondary"]
                    self.currentItemIndex = "secondary"
                else:
                    self.currentItem = self.inventory["primary"]
                    self.currentItemIndex = "primary"
            elif keys[keybinds["reload"]]:
                if self.currentItem != None and self.currentItem.type ==\
                      "guns" and not self.currentItem.reloading:
                    if self.inventory["ammo"][self.currentItem.data["name"]] > 0:
                        self.currentItem.reloading = True
                        self.soundChannel.play(self.currentItem.sounds["reload"])
        
        #TESTING FOR HEALTHBAR(REMOVE)
        if keys[pygame.K_COMMA]:
            self.health -=1
        if keys[pygame.K_PERIOD]:
            self.health +=1

        # Button cooldown
        self.cooldown.update(deltaTime)
        
        # Reloading
        if self.currentItem != None and self.currentItem.type == "guns" and \
            self.currentItem.reloading:
            self.currentItem.reloadTime -= deltaTime
            
            if self.currentItem.reloadTime <= 0:
                self.currentItem.reloading = False
                self.currentItem.reloadTime = self.currentItem.data[
                    "reloadSpeed"]
                
                ammo = self.inventory["ammo"][self.currentItem.data["name"]]
                maxClip = self.currentItem.data["clip"]
                clip = self.currentItem.clip

                ammo -= maxClip - clip
                clip = maxClip

                if ammo < 0:
                    clip += ammo
                    ammo = 0
                
                self.inventory["ammo"][self.currentItem.data["name"]] = ammo
                self.currentItem.clip = clip

    def collision(self, direction):
        '''
        Function checks for and handles collision 
        '''
        # Check if colliding
        for i in self.collisions:
            if hasattr(i, "hitbox") and i.hitbox.colliderect(self.hitbox):
                if direction == "horizontal":
                    if self.direction.x > 0:
                        self.hitbox.right = i.hitbox.left
                    
                    if self.direction.x < 0:
                        self.hitbox.left = i.hitbox.right
                    
                    self.rect.centerx = self.hitbox.centerx
                    self.position.x = self.hitbox.centerx
                else:
                    if self.direction.y > 0:
                        self.hitbox.bottom = i.hitbox.top
                    
                    if self.direction.y < 0:
                        self.hitbox.top = i.hitbox.bottom
                    
                    self.rect.centery = self.hitbox.centery
                    self.position.y = self.hitbox.centery

    def move(self, deltaTime):
        '''
        Function moves player controlled character
        '''
        # Normalize vector
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()

        # Horizontal movement
        self.position.x += self.direction.x * self.speed * deltaTime
        self.hitbox.centerx = round(self.position.x)
        self.rect.centerx = self.hitbox.centerx
        self.collision("horizontal")

        # Vertical movement
        self.position.y += self.direction.y * self.speed * deltaTime
        self.hitbox.centery = round(self.position.y)
        self.rect.centery = self.hitbox.centery
        self.collision("vertical")

        # Play footstep
        if self.direction != pygame.math.Vector2(0) and not self.footstepTimer.active:
            self.soundChannel.play(self.sounds["footsteps"][self.footstepSound][str(self.footstepIndex)])
            self.footstepTimer.start()

            self.footstepIndex += 1

            if self.footstepIndex > 2:
                self.footstepIndex = 0

        # Update footstep timer
        self.footstepTimer.update(deltaTime)
    
    def updateOffset(self, offset):
        '''
        Refreshes self.offset
        '''
        self.offset = offset
    
    def update(self, deltaTime):
        '''
        Updates certain key variables
        '''
        # Update player
        self.input(deltaTime)
        self.move(deltaTime)
        self.animate(deltaTime)

        # Update the currently held item
        if self.currentItem != None:
            self.currentItem.update(deltaTime, self.offset)
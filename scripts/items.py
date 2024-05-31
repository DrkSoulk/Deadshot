import pygame, math
from settings import *
from misc import *
from random import uniform

items = {
    "guns": {
        "nerfGun": {
            "fireRate": "semi",
            "type": "nerfDart",
            "scale": 2,
            "offset": 0.1,
            "cooldown": 0.4,
            "clip": 7,
            "speed": 75,
            "reloadSpeed": 1,
            "spread": 0
        },
        "ak47": {
            "fireRate": "auto",
            "type": "bullet",
            "scale": 1,
            "offset": 0,
            "cooldown": 0.15,
            "clip": 30,
            "speed": 75,
            "reloadSpeed": 1.5,
            "spread": 3
        }
    }
}

class bulletHole(pygame.sprite.Sprite):
    def __init__(self, position):
        # Initialize the bullet hole
        super().__init__()

        # Bullet hole setup
        self.image = scaleImage(pygame.image.load("sprites/vfx/bulletHole.png"), 1.2).convert_alpha()
        self.rect = self.image.get_rect(center = position)
        self.zIndex = layers["vfx"]
        self.lifetime = 4
    
    def update(self, deltaTime):
        # Decrease lifetime
        self.lifetime -= deltaTime

        # Destroy bullet hole
        if self.lifetime <= 0:
            self.kill()

class projectile(pygame.sprite.Sprite):
    def __init__(self, type, position, angle, data):
        # Initialize the projectile
        super().__init__()

        # Projectile setup
        self.zIndex = layers["projectiles"]
        self.originalImage = scaleImage(pygame.image.load("sprites/projectiles/" + type + ".png"), data["scale"]).convert_alpha()
        self.rect = self.originalImage.get_rect(center = position)
        self.position = position

        # Velocity
        self.angle = math.radians(angle)
        self.velocity = pygame.math.Vector2(math.cos(self.angle) * data["speed"] * 10, math.sin(self.angle) * data["speed"] * 10)

        # Rotate image
        self.image = pygame.transform.rotate(self.originalImage, -math.degrees(math.atan2(self.velocity.y, self.velocity.x)))
        self.rect = self.image.get_rect(center = self.rect.center)

        # Collisions
        self.collisions = None
        
    def update(self, deltaTime):
        # Update position of projectile
        self.position += self.velocity * deltaTime
        self.rect.center = (int(self.position.x), int(self.position.y))

        # Check for collision
        for i in self.collisions:
            if hasattr(i, "hitbox") and i.hitbox.colliderect(self.rect):
                # Create bullet hole
                spawn = pygame.math.Vector2()

                if self.velocity.x > 0:
                    spawn.x = self.position.x + (self.image.get_width() / 2)
                else:
                    spawn.x = self.position.x - (self.image.get_width() / 2)
                
                if self.velocity.y > 0:
                    spawn.y = self.position.y + (self.image.get_height() / 2)
                else:
                    spawn.y = self.position.y - (self.image.get_height() / 2)

                vfx.add(bulletHole(pygame.math.Vector2(spawn.x, spawn.y) + self.velocity * deltaTime))

                # Destroy projectile
                self.kill()

                return

class item(pygame.sprite.Sprite):
    def __init__(self, name, position):
        # Item setup
        self.name = name
        self.type = ""
        self.playerPosition = position
        self.itemPosition = pygame.math.Vector2()
        self.originalImage = pygame.image.load("sprites/items/" + name + ".png").convert_alpha()
        self.angle = 0
        self.flipped = False
        self.data = None
        self.mouseDownCheck = False

        # Get item data
        for i, v in items.items():
            for a, b in v.items():
                if a == name:
                    self.type = i
                    self.data = b

        # Scale image
        self.originalImage = scaleImage(self.originalImage, 2)

        # Image setup
        self.image = self.originalImage
        self.rect = self.image.get_rect(center = position)

        # Cooldown setup
        self.cooldown = timer(self.data["cooldown"])
        
        # Ammo setup
        self.clip = self.data["clip"]
        self.reloading = False
        self.reloadTime = self.data["reloadSpeed"]

        # Sound setup
        self.sounds = importSounds("sounds/items/" + name, "guns")
        self.fireIndex = 0

    def use(self):
        if self.type == "guns" and self.clip > 0 and not self.reloading:
            # Projectile setup
            spread = self.angle + uniform(-self.data["spread"], self.data["spread"])
            spawn = self.itemPosition + pygame.math.Vector2(math.cos(math.radians(spread)), math.sin(math.radians(spread))) * (self.originalImage.get_width() / 2)
            projectiles.add(projectile(self.data["type"], spawn, spread, self.data))
            
            # Remove ammo from clip
            self.clip -= 1

            # Play sound
            self.sounds["fire" + str(self.fireIndex)].play()
            self.fireIndex += 1

            if self.fireIndex > 2:
                self.fireIndex = 0

    def update(self, deltaTime, offset):
        # Get the mouse
        mouse = pygame.math.Vector2(pygame.mouse.get_pos())
        mouseButton = pygame.mouse.get_pressed()

        # Get angle
        self.angle = math.degrees(math.atan2(mouse.y - (self.playerPosition.y - offset.y), mouse.x - (self.playerPosition.x - offset.x)))

        # Get item position
        self.itemPosition = pygame.math.Vector2((math.cos(math.radians(self.angle)) * 16) + self.playerPosition.x, (math.sin(math.radians(self.angle)) * 16) + self.playerPosition.y)

        # Rotate item
        if mouse.x < self.playerPosition.x - offset.x:
            # Flip and rotate item
            self.image = pygame.transform.rotate(self.originalImage, self.angle)
            self.image = pygame.transform.flip(self.image, 0, 1)
        else:
            # Rotate item
            self.image = pygame.transform.rotate(self.originalImage, -self.angle)
            
        # Update rect
        self.rect = self.image.get_rect(center = self.itemPosition + pygame.math.Vector2(0, 3))
        self.rect.center -= offset

        # Use the item
        if mouseButton[0]:
            if not self.cooldown.active:
                if self.type == "guns" and self.data["fireRate"] == "semi":
                    if not self.mouseDownCheck:
                        self.use()
                        self.cooldown.start()
                        self.mouseDownCheck = True
                else:
                    self.use()
                    self.cooldown.start()
        else:
            self.mouseDownCheck = False
        
        # Item cooldown
        self.cooldown.update(deltaTime)
import pygame, math
from settings import *
from misc import *
from random import uniform

items = {
    "guns": {
        "nerfGun": {
            "name": "nerfGun",
            "fireRate": "semi",
            "type": "nerfDart",
            "scale": 2,
            "offset": 0.1,
            "cooldown": 0.4,
            "clip": 7,
            "speed": 75,
            "reloadSpeed": 1,
            "spread": 4
        },
        "pistol": {
            "name": "pistol",
            "fireRate": "semi",
            "type": "smallBullet",
            "scale": 1.5,
            "offset": 0.1,
            "cooldown": 0.25,
            "clip": 7,
            "speed": 75,
            "reloadSpeed": 0.6,
            "spread": 5
        },
        "smg": {
            "name": "smg",
            "fireRate": "auto",
            "type": "bullet",
            "scale": 2,
            "offset": 0,
            "cooldown": 0.08,
            "clip": 25,
            "speed": 75,
            "reloadSpeed": 1.2,
            "spread": 8
        },
        "rifle": {
            "name": "rifle",
            "fireRate": "auto",
            "type": "bullet",
            "scale": 2,
            "offset": 0,
            "cooldown": 0.15,
            "clip": 30,
            "speed": 75,
            "reloadSpeed": 1.5,
            "spread": 7
        },
        "shotgun": {
            "name": "shotgun",
            "fireRate": "semi",
            "type": "pellet",
            "scale": 2,
            "offset": 0.5,
            "cooldown": 0.7,
            "clip": 2,
            "speed": 60,
            "reloadSpeed": 0.8,
            "spread": [10, 10]
        },
        "sniper": {
            "name": "sniper",
            "fireRate": "semi",
            "type": "heavyBullet",
            "scale": 2,
            "offset": 0,
            "cooldown": 1,
            "clip": 3,
            "speed": 200,
            "reloadSpeed": 2,
            "spread": 0
        },
        "revolver": {
            "name": "revolver",
            "fireRate": "semi",
            "type": "heavyBullet",
            "scale": 2,
            "offset": 0,
            "cooldown": 0.8,
            "clip": 6,
            "speed": 100,
            "reloadSpeed": 1.5,
            "spread": 0
        },
        "tommyGun": {
            "name": "tommyGun",
            "fireRate": "auto",
            "type": "bullet",
            "scale": 2,
            "offset": 0,
            "cooldown": 0.12,
            "clip": 50,
            "speed": 75,
            "reloadSpeed": 1.5,
            "spread": 10
        },
        "pea": {
            "name": "pea",
            "fireRate": "semi",
            "type": "pea",
            "scale": 2,
            "offset": 0,
            "cooldown": 0.4,
            "clip": 5,
            "speed": 75,
            "reloadSpeed": 0.8,
            "spread": 5
        },
        "tshirt": {
            "name": "tshirt",
            "fireRate": "semi",
            "type": "tshirt",
            "scale": 2,
            "offset": 0,
            "cooldown": 0,
            "clip": 1,
            "speed": 120,
            "reloadSpeed": 1.2,
            "spread": 2
        },
        "guitar": {
            "name": "guitar",
            "fireRate": "semi",
            "type": ["musicNote1", "musicNote2", "musicNote3"],
            "scale": 2,
            "offset": 0,
            "cooldown": 0,
            "clip": 16,
            "speed": 60,
            "reloadSpeed": 0.6,
            "spread": 7
        },
        "letter": {
            "name": "letter",
            "fireRate": "auto",
            "type": ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"],
            "scale": 1.5,
            "offset": 0,
            "cooldown": 0.2,
            "clip": 20,
            "speed": 55,
            "reloadSpeed": 0.7,
            "spread": 5
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
        self.originalImage = scaleImage(pygame.image.load("sprites/projectiles/" + type + ".png"), 1.5).convert_alpha()
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

        # Image setup
        self.originalImage = scaleImage(pygame.image.load("sprites/items/" + name + ".png").convert_alpha(), self.data["scale"])
        self.image = self.originalImage
        self.rect = self.image.get_rect(center = position)
        self.projectileIndex = 0

        # Cooldown setup
        self.cooldown = timer(self.data["cooldown"])
        
        # Ammo setup
        self.clip = self.data["clip"]
        self.reloading = False
        self.reloadTime = self.data["reloadSpeed"]

        # Sound setup
        self.soundChannel = pygame.mixer.Channel(1)
        self.sounds = importSounds("sounds/items/" + name)
        self.fireIndex = 0

        # Set volume
        self.soundChannel.set_volume(mixer["guns"])

    def fireGun(self, spread):
        # Projectile setup
        newSpread = self.angle + uniform(-spread, spread)
        spawn = self.itemPosition + pygame.math.Vector2(math.cos(math.radians(newSpread)), math.sin(math.radians(newSpread))) * (self.originalImage.get_width() / 2)
        
        # Get the projectile image
        image = self.data["type"]

        if type(image) == str:
            projectiles.add(projectile(self.data["type"], spawn, newSpread, self.data))
        else:
            projectiles.add(projectile(self.data["type"][self.projectileIndex], spawn, newSpread, self.data))

            self.projectileIndex += 1

            if self.projectileIndex > len(self.data["type"]) - 1:
                self.projectileIndex = 0

        # Play sound
        self.soundChannel.play(self.sounds["fire" + str(self.fireIndex)])
        self.fireIndex += 1

        if self.fireIndex > 2:
            self.fireIndex = 0

    def use(self):
        if self.type == "guns" and self.clip > 0 and not self.reloading:
            # Fire gun
            if type(self.data["spread"]) != int:
                for i in range(1, self.data["spread"][0]):
                    self.fireGun(self.data["spread"][1])
            else:
                self.fireGun(self.data["spread"])
            
            # Remove ammo from clip
            self.clip -= 1

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
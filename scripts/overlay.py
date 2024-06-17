import pygame
from settings import *
from items import items

class overlay(pygame.sprite.Sprite):
    def __init__(self):
        # Overlay setup
        self.overlay = pygame.surface.Surface(resolution - overlayOffset, \
                                              pygame.SRCALPHA, 32\
                                                ).convert_alpha()
        self.rect = self.overlay.get_rect(center = middleScreen)
        
        # Import font
        self.basicFont = pygame.freetype.Font("fonts/basic.ttf", fontSize)

        #Load bullet image
        self.bulletImage = pygame.image.load("sprites/hud/Bullet.png"\
                                             ).convert_alpha()

        # Set up menus
        self.selector = 0
        self.submenus = ['map', 'weapon', 'start']
        self.menublurb = ["press Esc to quit","press P to pause/resume",
                          "press up/down and enter to select"]
    
    def drawText(self, text, position = 1):
        # Get overlay size
        size = pygame.math.Vector2(self.overlay.get_size())

        # Draw text
        textSize = self.basicFont.get_rect(text)
        self.basicFont.render_to(self.overlay, (size.x - textSize.width,\
                                                 size.y - (textSize.height *\
                                                            position)), \
                                                    text, (255, 255, 255))

    def drawHealth(self, health, position = 3):
        # Get overlay size
        size = pygame.math.Vector2(self.overlay.get_size())
        
        # Avoids <0 or >255 error
        if health < 0:
            health = 0
        elif health > 100:
            health = 100
        healthbar = pygame.surface.Surface((health*2, 20))

        # Colour and draw healthbar
        red = int(255-health*2.55)
        green = int(health*2.55)
        healthbar.fill((red, green,0))
        healthbarSize = healthbar.get_rect()
        self.overlay.blit(healthbar,(size.x - healthbarSize.width, size.y - \
                                     (healthbarSize.height * position)))
        
    def drawAmmo(self, clip, ammo, position = 1):
        # Get overlay size
        size = pygame.math.Vector2(self.overlay.get_size())
        # Create surface for icon blit

        ammobar = pygame.surface.Surface((clip*5, 20)).convert_alpha()
        ammobar.fill((0,0,0,0))

        # Draw bullets
        for ammocount in range(clip):
            ammobar.blit(self.bulletImage, (ammocount*5, 0))
        
        # Draw text and ammobar
        ammobarSize = ammobar.get_rect()
        textSize = self.basicFont.get_rect((ammo))
        self.basicFont.render_to(self.overlay, (size.x - textSize.width,\
                                                 size.y - (textSize.height \
                                                           * position)), \
                                                        ammo, (255, 255, 255))
        self.overlay.blit(ammobar,(size.x - ammobarSize.width - \
                                   textSize.width - 3, size.y - \
                                    (ammobarSize.height * position)))




    def update(self, player):
        # Clear overlay
        self.overlay.fill((0, 0, 0, 0))

        # Get overlay size
        size = pygame.math.Vector2(self.overlay.get_size())
        
        # Draw health display
        self.drawHealth(player.health)

        # Draw ammo display
        if player.currentItem.type == "guns":
            self.drawAmmo((player.currentItem.clip), ' l ' + \
                          str(player.inventory["ammo"]\
                              [player.currentItem.data["name"]]))
        
        # Return to be drawn
        return self.overlay, self.rect
    

    def drawMenu(self):
        self.overlay.fill((0, 0, 0, 0))
        selected = self.submenus[self.selector]

        for menu in self.submenus:
            col = (255,255,255)
            if selected == menu:
                col = selectorColour
            textSize = self.basicFont.get_rect(menu)
            self.basicFont.render_to(self.overlay, 
                                     (middleScreen.x - 0.5*textSize.width, \
                                      middleScreen.y -90 +self.submenus.index\
                                        (menu)*fontSize), menu,(col))
            for i in self.menublurb:
                self.drawText(i, self.menublurb.index(i)*2 + 1)

        return self.overlay, self.rect


    def select(self, level):
        # Create item list
        itemlist = []
        for i in items['guns']:
            itemlist.append(i)
        itemlist.append('back')
        
        selected = self.submenus[self.selector]
        
        if selected == 'map':
            self.submenus = maplist
            self.menublurb = [level.currentmap,
                              "current map:"]

        elif self.submenus == maplist:
            if not selected == 'back':
                level.unloadedMap = selected
            else:
                self.submenus = ['map', 'weapon', 'start']
                self.menublurb = ["press Esc to quit",\
                                  "press P to pause/resume",
                                  "press up/down and enter to select"]

        elif selected == 'weapon':
            self.submenus = itemlist
            self.menublurb = [level.player.currentItemIndex,
                              "currently selecting:"]

        elif self.submenus == itemlist:
            if not selected == 'back':
                if level.player.currentItemIndex == 'primary':
                    level.primary = selected
                else:
                    level.secondary = selected
            else:
                self.submenus = ['map', 'weapon', 'start']
                self.menublurb = ["press Esc to quit",\
                                  "press P to pause/resume",
                                  "press up/down and enter to select"]
                

        elif selected == 'start':
            level.load(level.unloadedMap)
            level.pause = False
        self.selector = 0


    def menuDown(self):
        if not self.selector >= len(self.submenus) - 1:
            self.selector += 1
        else:
            self.selector = 0


    def menuUp(self):
        if not self.selector <= 0:
            self.selector -= 1
        else:
            self.selector = len(self.submenus) - 1
'''
This module contains the game class.
This class contains central functions and the main game loop.
'''

import pygame, sys  
from settings import *
from level import *

class game:
    '''
    Class for main loop and certain central variables/functions
    '''
    def __init__(self):
        # Initialize pygame
        pygame.init()
        pygame.font.init()
        pygame.display.set_caption("Deadshot (Testing)")

        # Create game objects and variables
        self.window = pygame.display.set_mode(resolution)
        self.uptime = pygame.time.Clock()
        self.level = level()
    
    def run(self):
        '''
        Main loop
        '''
        while True:
            for i in pygame.event.get():
                # Quit pygame
                if i.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif i.type == pygame.KEYDOWN:
                    if i.key == keybinds["endGame"]:
                        pygame.quit()
                        sys.exit()
                    if i.key == keybinds["pause"]:
                        self.level.pause = (not self.level.pause)
                    
                    # UI
                    if self.level.pause:
                        if i.key == keybinds['select']:
                            self.level.overlay.select(self.level)
                        if i.key == keybinds['menuUp']:
                            self.level.overlay.menuUp()
                        if i.key == keybinds['menuDown']:
                            self.level.overlay.menuDown()
            
            # Getting the delta time
            deltaTime = self.uptime.tick() / 1000

            # Running the level
            if self.level.pause:
                self.level.menu()
            else:
                self.level.run(deltaTime)                

            # Updating the screen
            pygame.display.update()

if __name__ == "__main__":
    game().run()
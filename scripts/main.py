import pygame, sys  
from settings import *
from level import *

class game:
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
            
            # Getting the delta time
            deltaTime = self.uptime.tick() / 1000

            # Running the level
            self.level.run(deltaTime)

            # Updating the screen
            pygame.display.update()

if __name__ == "__main__":
    game().run()
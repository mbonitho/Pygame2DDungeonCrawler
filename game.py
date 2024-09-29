import pygame
import sys
import asyncio

from settings.constants import *
from states.explorationState import ExplorationState

class Game:

    def __init__(self):
        # Initialize Pygame
        pygame.init()

        # Create the screen
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("2D dungeon (hopefully)")

        self.delta_time = 0

        # Set the 1st state
        self.currentState = ExplorationState(self.screen)

    async def run(self):

        # Main game loop
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.currentState.input()
            self.currentState.update(self.delta_time)

            # Clear the screen
            self.screen.fill(BLACK)
            # Draw current state
            self.currentState.draw()
            # Update the display
            pygame.display.flip()

            # Cap the frame rate
            self.delta_time = pygame.time.Clock().tick(60)
            await asyncio.sleep(0)


import asyncio
from game import Game

if __name__ == "__main__":
    game = Game()
    asyncio.run(game.run())
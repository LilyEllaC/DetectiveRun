import pygame 
import constants as c
import utility
import asyncio
import intro
import playing
import end
from enum import Enum


# pylint: disable=no-member
pygame.init()

#running
running=True

class GameStates(Enum):
    INTRO=1
    PLAYING=2
    END=3

async def main():
    global running
    gameState=GameStates.INTRO

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if gameState==GameStates.INTRO:
                if event.type==pygame.MOUSEBUTTONDOWN:
                    if intro.startButton.isHovered:
                        gameState=GameStates.PLAYING
            if gameState==GameStates.PLAYING:
                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_SPACE and playing.crow.y==playing.crow.floor-playing.crow.height-5:
                        playing.crow.yVelocity=-20
                        playing.crow.jumpPressed=True


        if gameState==GameStates.INTRO:
            intro.showIntro()
        elif gameState==GameStates.PLAYING:
            playing.playGame()
        elif gameState==GameStates.END:
            end.endGame()

        #ending stuff
        pygame.display.flip()
        c.clock.tick(c.FPS)
        await asyncio.sleep(0)


if __name__ == "__main__":
    asyncio.run(main())
    pygame.quit()
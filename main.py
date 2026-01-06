import time

import pygame
import constants as const
import help
import asyncio
import intro
import playing
import end
from enum import Enum

import utility
import vector2

# pylint: disable=no-member
pygame.init()

#running
running=True

class GameStates(Enum):
    INTRO=1
    PLAYING=2
    END=3
    HELP=4

async def main():
    global running
    gameState=GameStates.INTRO

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if gameState==GameStates.INTRO:
                if event.type==pygame.MOUSEBUTTONDOWN:
                    if intro.startButton.isHovered():
                        gameState=GameStates.PLAYING
                    elif intro.helpButton.isHovered():
                        await utility.fadeOutResource(intro.bg)

                        gameState = GameStates.HELP
                        help.showHelp()

                        await utility.fadeInResource(help.bg)
                    elif intro.exitButton.isHovered():
                        running=False

            if gameState==GameStates.PLAYING:
                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_SPACE and playing.crow.y==playing.crow.floor-playing.crow.height-5:
                        playing.crow.yVelocity=-20*c.FPS_SCALING
                        playing.crow.jumpPressed=True
                    if event.key==pygame.K_DOWN:
                        playing.crow.faster=1*c.FPS_SCALING
                if event.type==pygame.KEYUP:
                    if event.key==pygame.K_DOWN:
                        playing.crow.faster=0

        

        if gameState==GameStates.INTRO:
            intro.showIntro()
        elif gameState==GameStates.PLAYING:
            playing.playGame()
            #ending the gameplay
            if playing.crow.hasCollided(playing.obstacles):
                gameState=GameStates.END
        elif gameState==GameStates.END:
            end.endGame()
        elif gameState==GameStates.HELP:
            help.showHelp()

        #ending stuff
        pygame.display.flip()
        const.clock.tick(const.FPS)
        await asyncio.sleep(0)


if __name__ == "__main__":
    asyncio.run(main())
    pygame.quit()
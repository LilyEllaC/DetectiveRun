import pygame
import constants as const
import resource
import utility
import spriteClasses
import vector2

startButton = spriteClasses.Button(800, const.HEIGHT / 2 - 40, 320, 60, "Start", const.FONT20, const.WHITE, const.GRAY, True)
startButton.textColour = const.BLACK

exitButton = spriteClasses.Button(800, const.HEIGHT / 2 + 40, 320, 60, "Exit", const.FONT20, const.WHITE, const.GRAY, True)
exitButton.textColour = const.LIGHT_RED

def showIntro():
    bg = resource.Resource("assets/start.png", vector2.Vector2(2304, 1296), 1, 1, 1, 0.7, vector2.Vector2(0, 0))
    bg.drawImage(const.screen, vector2.Vector2(0, 0))

    utility.toScreen("Detective Run", const.FONT60, const.BLACK, const.WIDTH / 2, 100)

    startButton.draw()
    exitButton.draw()
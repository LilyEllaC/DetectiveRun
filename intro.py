import pygame
import constants as const
import main
import resource
import utility
import spriteClasses
import vector2

startButton = spriteClasses.Button(800, const.HEIGHT / 2 - 80, 320, 60, "Start", const.FONT20, const.WHITE, const.GRAY, True)
startButton.textColour = const.BLACK

helpButton = spriteClasses.Button(800, const.HEIGHT / 2, 320, 60, "How to play?", const.FONT20, const.WHITE, const.GRAY, True)
helpButton.textColour = const.BLACK

exitButton = spriteClasses.Button(800, const.HEIGHT / 2 + 80, 320, 60, "Exit", const.FONT20, const.WHITE, const.GRAY, True)
exitButton.textColour = const.LIGHT_RED

bg = resource.Resource("assets/start.png", vector2.Vector2(2304, 1296), 1, 1, 1, 0.7, vector2.Vector2(0, 0))
crow = resource.Resource("assets/crow-Sheet.png", vector2.Vector2(64, 64), 8, 14, 0, 4, vector2.Vector2(0, 0))
crow.animation_cooldown = 100

def showIntro():
    bg.drawImage(const.screen, vector2.Vector2(0, 0))

    utility.toScreen("Detective Run", const.FONT60, const.BLACK, const.WIDTH / 2, 100)

    # Crow animation
    crow.drawImage(const.screen, vector2.Vector2(50, const.HEIGHT / 2 - 245))

    current_time = pygame.time.get_ticks()
    if current_time - crow.last_update >= crow.animation_cooldown:
        crow.last_update = current_time

        if crow.frame == 25:
            crow.frame = 0
        if crow.frame == 9:
            crow.frame = 17
        else:
            crow.frame += 1

    startButton.draw()
    helpButton.draw()
    exitButton.draw()
import pygame.draw

import resource
import const as const
import utility
import vector2

bg = resource.Resource(
    "assets/help.png", vector2.Vector2(2304, 1296), 1, 1, 1, 0.7, vector2.Vector2(0, 0)
)
backButton = pygame.Surface((45, 40), pygame.SRCALPHA)
backButton.fill((255, 255, 255, 0))


def showHelp():
    bg.drawImage(const.screen, vector2.Vector2(0, 0))

    utility.toScreen("How to play?", const.FONT60, const.BLACK, const.WIDTH / 2, 100)

    pygame.draw.line(const.screen, const.BLACK, (80, 50), (40, 50), 4)
    pygame.draw.line(const.screen, const.BLACK, (40, 50), (60, 60), 4)
    pygame.draw.line(const.screen, const.BLACK, (40, 50), (60, 40), 4)

    const.screen.blit(backButton, (38, 30))

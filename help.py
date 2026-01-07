import pygame
import resources
import spriteClasses
import const
import utility
import vector2

bg = resources.Resource(
    "assets/help.png", vector2.Vector2(2304, 1296), 1, 1, 1, 0.7, vector2.Vector2(0, 0)
)
backButton = spriteClasses.Button(
    38,
    30,
    50,
    50,
    "",
    const.FONT40,
    (0, 0, 0, 0),
    (0, 0, 0, 0),
    False,
)


def render():
    bg.draw_image(const.screen, vector2.Vector2(0, 0))

    utility.toScreen("How to play?", const.FONT60, const.BLACK, const.WIDTH / 2, 100)

    # Custom drawing for the arrow
    pygame.draw.line(const.screen, const.BLACK, (80, 50), (40, 50), 4)
    pygame.draw.line(const.screen, const.BLACK, (40, 50), (60, 60), 4)
    pygame.draw.line(const.screen, const.BLACK, (40, 50), (60, 40), 4)

    # Invisible but interactive button
    backButton.draw()

    utility.toScreen3("After uncovering the murderer’s identity, you begin the chase.",
                      "Stay focused: while pursuing him, your colleagues will question you to gather crucial information about his escape route.",
                      "One mistake like crashing into an obstacle or answering incorrectly and the chase is over.",
                     const.FONT20, const.BLACK, const.WIDTH / 2, 200)

    utility.toScreen("Controls", const.FONT30, const.BLACK, const.WIDTH / 2, 290)

    utility.toScreen3("Space - Jump",
                      "Arrow down - Fall faster",
                      "-------",
                      const.FONT20, const.BLACK, const.WIDTH / 2, 380)

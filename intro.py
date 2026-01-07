import pygame
import const
import resources
import utility
import spriteClasses
import vector2

startButton = spriteClasses.Button(
    800,
    const.HEIGHT / 2 - 80,
    320,
    60,
    "Start",
    const.FONT20,
    const.WHITE,
    const.GRAY,
    True,
)
startButton.textColour = const.BLACK

helpButton = spriteClasses.Button(
    800,
    const.HEIGHT / 2,
    320,
    60,
    "How to play?",
    const.FONT20,
    const.WHITE,
    const.GRAY,
    True,
)
helpButton.textColour = const.BLACK

exitButton = spriteClasses.Button(
    800,
    const.HEIGHT / 2 + 80,
    320,
    60,
    "Exit",
    const.FONT20,
    const.WHITE,
    const.GRAY,
    True,
)
exitButton.textColour = const.LIGHT_RED

bg = resources.Resource(
    "assets/start.png", vector2.Vector2(2304, 1296), 1, 1, 1, 0.7, vector2.Vector2(0, 0)
)

crow = resources.Resource(
    "assets/crow-Sheet.png", vector2.Vector2(64, 64), 8, 14, 0, 4, vector2.Vector2(0, 0)
)
crow.animation_cooldown = 100


def render():
    bg.draw_image(const.screen, vector2.Vector2(0, 0))

    s = pygame.Surface((500, const.HEIGHT), pygame.SRCALPHA)  # per-pixel alpha
    s.fill((0, 0, 0, 128))  # notice the alpha value in the color
    const.screen.blit(s, (700, 0))

    utility.toScreen("Detective Run", const.FONT60, const.WHITE, 950, 150)

    # Crow animation
    const.crow.draw_image(const.screen, vector2.Vector2(50, const.HEIGHT / 2 - 245))

    current_time = pygame.time.get_ticks()
    if current_time - const.crow.last_update >= const.crow.animation_cooldown:
        const.crow.last_update = current_time

        if const.crow.frame >= 25:
            const.crow.frame = 0
        if const.crow.frame == 9:
            const.crow.frame = 17
        else:
            const.crow.frame += 1

    startButton.draw()
    helpButton.draw()
    exitButton.draw()

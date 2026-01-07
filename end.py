import pygame
import const
import utility
import playing
from spriteClasses import Button

pygame.init()

restartButton = Button(
    const.WIDTH // 2 - 100,
    const.HEIGHT - 120,
    200,
    100,
    "RESTART",
    const.FONT40,
    const.GREEN,
    const.DARK_YELLOW,
    True,
)


def render():
    const.screen.fill(const.DARK_PURPLE)
    utility.toScreen("You got hit :(", const.FONT40, const.WHITE, const.WIDTH // 2, 100)

    if playing.crow.points < 10:
        text = "How is a score that low even possible?"
    elif playing.crow.points < 20:
        text = "Were you even playing?"
    elif playing.crow.points < 30:
        text = "You're doing good"
    elif playing.crow.points < 40:
        text = "You ran for a while"
    elif playing.crow.points < 50:
        text = "You must be exhausted"
    elif playing.crow.points < 100:
        text = "Wow, you must have practiced a long time"
    elif playing.crow.points < 200:
        text = "That was great!"
    elif playing.crow.points < 500:
        text = "Wow, I didn't even know a score that high was possible"
    elif playing.crow.points < 2000:
        text = "Cheater."
    else:
        text = "Cheater."

    utility.toScreen(
        text, const.FONT30, const.GREEN, const.WIDTH // 2, const.HEIGHT // 2
    )
    restartButton.draw()

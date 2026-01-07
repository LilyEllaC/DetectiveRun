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
    utility.toScreen("You had a score of: "+str(round(playing.crow.points)), const.FONT30, const.YELLOW, const.WIDTH//2, 150)


    if playing.crow.points < 10:
        text = "How is a score that low even possible?"
    elif playing.crow.points < 20:
        text = "Were you even playing?"
    elif playing.crow.points < 50:
        text = "You're doing good"
    elif playing.crow.points < 100:
        text = "You ran for a while"
    elif playing.crow.points < 200:
        text = "You must be exhausted"
    elif playing.crow.points < 300:
        text = "Wow, you must have practiced a long time"
    elif playing.crow.points < 500:
        text = "That was great!"
    elif playing.crow.points < 1000:
        text = "Wow, I didn't even know a score that high was possible"
    elif playing.crow.points < 50000:
        text = "Cheater."
    else:
        text = "Cheater."

    utility.toScreen(
        text, const.FONT30, const.GREEN, const.WIDTH // 2, const.HEIGHT // 2
    )
    restartButton.draw()

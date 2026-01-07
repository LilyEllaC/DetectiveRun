import pygame
import const as c
import utility
import playing
from spriteClasses import Player, Button
# pylint: disable=no-member
pygame.init()

restartButton=Button(c.WIDTH//2, c.HEIGHT-100, 200, 100, "RESTART", c.FONT40, c.GREEN, c.DARK_YELLOW, True)

def endGame():
  c.screen.fill(c.DARK_PURPLE)
  utility.toScreen("You got hit :(", c.FONT40, c.WHITE, c.WIDTH // 2, 100)

  if True:
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

	utility.toScreen(text, c.FONT30, c.GREEN, c.WIDTH // 2, c.HEIGHT // 2)#button
  restartButton.draw()
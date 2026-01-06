import pygame 
import constants as c
import utility
from spriteClasses import Player
# pylint: disable=no-member
pygame.init()

#crow
crow=Player(100, c.HEIGHT-50, 100, 100, 1)

def playGame():
    c.screen.fill(c.ORANGE)
    crow.draw()
    print(crow.x, crow.y)

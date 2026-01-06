import pygame 
import constants as c
import utility
from spriteClasses import Player
# pylint: disable=no-member
pygame.init()

#crow
crow=Player(150, 100, 100, 1)
sprites=pygame.sprite.Group()
sprites.add(crow)


#playing
def playGame():
    c.screen.fill(c.ORANGE)

    #moving the crow
    crow.move()
    crow.jump()
    
    #drawing it
    sprites.draw(c.screen)

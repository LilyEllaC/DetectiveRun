import pygame 
import constants as c
import utility
from spriteClasses import Player, Obstacle
# pylint: disable=no-member
pygame.init()

#having the obstacles speed up
velocity=-5*c.FPS_SCALING

#sprites
crow=Player(150, 100, 100, 1*c.FPS_SCALING)
obstacleSize=50
obstacle1=Obstacle(c.WIDTH+20, obstacleSize, obstacleSize, velocity)
obstacle2=Obstacle(c.WIDTH+c.WIDTH//2, obstacleSize, obstacleSize, velocity)
sprites=pygame.sprite.Group()
sprites.add(crow)
sprites.add(obstacle1)
sprites.add(obstacle2)
obstacles=[obstacle1, obstacle2]


#playing
def playGame():
    global velocity
    c.screen.fill(c.ORANGE)

    #moving the crow
    crow.move()
    crow.jump()
    crow.displayPoints()

    #obstacles
    for obstacle in obstacles:
        obstacle.move(velocity)
        obstacle.reset()
    velocity-=0.01*c.FPS_SCALING
    
    #drawing it
    sprites.draw(c.screen)

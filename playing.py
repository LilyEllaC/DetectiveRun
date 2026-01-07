import pygame 
import constants as c
import resource
import vector2
from spriteClasses import Player, Obstacle, Question
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
tilemap=resource.Resource("assets/InteriorTilesLITE.png", vector2.Vector2(32, 32), 15, 15, 0, 13, vector2.Vector2(0, 0))

#restarting the variables
def reset():
    global velocity
    for obstacle in obstacles:
        obstacle.reset()
        obstacle.history.clear()
    obstacle2.x+=300
    crow.points=0
    velocity=0


#dealing with asking questions
history=[]
for obstacle in obstacles:
    for num in obstacle.history:
        history.append(num)
question=Question(c.WIDTH//2, c.HEIGHT//2, 300, 200, history)

#playing
def playGame():
    global velocity
    c.screen.fill(c.ORANGE)

    tilemap.drawImage(c.screen, vector2.Vector2(0, c.HEIGHT - 150))

    #moving the crow
    crow.move()
    crow.jump()
    crow.displayPoints()

    #obstacles
    for obstacle in obstacles:
        obstacle.move(velocity)
        if obstacle.x<-obstacle.width:
            obstacle.reset()
    velocity-=0.01*c.FPS_SCALING

    #asking a question
    question.draw()

    
    #drawing it
    sprites.draw(c.screen)

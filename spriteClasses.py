import pygame
import random
import constants as c

# pylint: disable=no-member
pygame.init()

#obstancle class
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, width, height, velocity):
        super().__init__()
        self.images=["list of images goes here"]
        imageNum=random.randInt(0, len(self.images))
        self.x=random.randInt(c.WIDTH, c.WIDTH+100)
        self.floor=c.HEIGHT-50
        self.width=width
        self.height=height
        self.velocity=velocity
        #loading the image
        self.image=pygame.image.load(self.images[imageNum])
        #self.image=pygame.tranform.scale(image, (width, height))
        self.rect=self.image.get_rect()
        self.height=self.image.get_height()
        self.y=self.floor-self.height
        self.rect.x=self.x
        self.rect.y=self.y

        #saving the history for the quizzes
        self.history=[imageNum]

    def move(self):
        self.x+=self.velocity
        
    def reset(self):
        if self.x<100:
            self.images=["list of images goes here"]
            imageNum=random.randInt(0, len(self.images))
            self.image=pygame.load.image(self.images[imageNum])
            self.height=self.image.get_height
            self.x=random.randInt(c.WIDTH, c.WIDTH+100)
            self.y=self.floor-self.height
            self.history.append(imageNum)

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, gravity):
        super().__init__()
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.gravity=gravity
        self.yVelocity=0

        image=pygame.image.load("crow.png")
        self.image=pygame.transform.scale(image, (width, height))
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
    
    def jump(self):
        if self.y<self.floor-self.height:
            self.yVelocity+=self.gravity
        else:
            self.yVelocity=0

    def moving(self):
        self.y+=self.yVelocity

    def hasCollided(self, obstacles):
        playerRect=self.image.get_rect()
        for obstacle in obstacles:
            if playerRect.colliderect(obstacle.rect):
                return True
        return False
    








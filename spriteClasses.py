import pygame
import random
import constants as c
import utility

# pylint: disable=no-member
pygame.init()

MINIMUM=c.HEIGHT-50

#obstancle class
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, width, height, velocity):
        super().__init__()
        self.images=["assets/crate.png"]
        imageNum=random.randint(0, len(self.images)-1)
        self.x=x
        self.bottom=MINIMUM
        self.width=width
        self.height=height
        self.velocity=velocity
        #loading the image
        self.image=pygame.image.load(self.images[imageNum])
        self.image=pygame.transform.scale(self.image, (width, height))
        self.rect=self.image.get_rect()
        self.height=self.image.get_height()
        self.y=self.bottom-self.height
        self.rect.x=self.x
        self.rect.y=self.y

        #saving the history for the quizzes
        self.history=[imageNum]

    def move(self, velocity):
        self.velocity=velocity
        self.x+=self.velocity
        self.rect.x=self.x
        self.rect.y=self.y
        
    def reset(self):
        self.images=["assets/crate.png"]
        imageNum=random.randint(0, len(self.images)-1)
        self.image=pygame.image.load(self.images[imageNum])
        self.image=pygame.transform.scale(self.image, (self.width, self.height))
        self.height=self.image.get_height()
        self.x=random.randint(c.WIDTH, c.WIDTH+100)
        self.y=self.bottom-self.height
        self.history.append(imageNum)

class Player(pygame.sprite.Sprite):
    def __init__(self, x, width, height, gravity):
        super().__init__()
        self.walks=["assets/crow.png"]
        self.walkNum=0
        self.jumps=["assets/crow.png"]
        self.jumpNum=0
        self.x=x
        self.width=width
        self.height=height*c.FPS_SCALING
        self.gravity=gravity
        self.floor=MINIMUM
        self.yVelocity=0
        self.jumpPressed=False
        self.faster=0
        self.points=0

        image=pygame.image.load(self.walks[self.walkNum])
        self.image=pygame.transform.scale(image, (width, height))
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.y=self.floor-self.height-5
    
    def jump(self):
        if self.jumpPressed:
            if self.y<self.floor-self.height:
                self.yVelocity+=self.gravity+self.faster
                #appearance
                self.image=pygame.image.load(self.jumps[self.jumpNum])
                self.jumpNum+=1
                if self.jumpNum>=len(self.jumps):
                    self.jumpNum=0
            #jump stopping
            else:
                self.yVelocity=0
                self.y=self.floor-self.height-5
                #appearance
                self.image=pygame.image.load(self.walks[self.walkNum])
                self.walkNum+=1
                if self.walkNum>=len(self.walks):
                    self.walkNum=0
                self.jumpPressed=False
            self.y+=self.yVelocity
    
    def move(self):
        self.rect.x=self.x
        self.rect.y=self.y
        self.image=pygame.transform.scale(self.image, (self.width, self.height))
        self.points+=0.1

    def hasCollided(self, obstacles):
        for obstacle in obstacles:
            if self.rect.colliderect(obstacle.rect):
                return True
        return False
    
    def displayPoints(self):
        utility.toScreen("Score: "+str(round(self.points)), c.FONT30, c.BLACK, c.WIDTH-100, 50)

class Button():
    def __init__(self, x, y, width, height, text, font, colour1, colour2, hasOutline: bool):
        self.rect = None
        self.x = x
        self.y = y

        self.width = width
        self.height = height

        self.text = text
        self.font = font

        self.colours = [colour1, colour2]
        self.colour = colour1
        self.textColour = c.WHITE

        self.hasOutline = hasOutline

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self):
        pygame.draw.rect(c.screen, self.colour, self.rect)

        if self.hasOutline:
            pygame.draw.rect(c.screen, c.BLACK, self.rect, 3)
        if self.isHovered():
            self.colour=self.colours[1]
        else:
            self.colour=self.colours[0]
        
        utility.toScreen(self.text, self.font, self.textColour, self.x + self.width // 2, self.y + self.height // 2)

    def isHovered(self):
        mouseX, mouseY = pygame.mouse.get_pos()

        if self.rect.collidepoint(mouseX, mouseY):
            return True

        return False







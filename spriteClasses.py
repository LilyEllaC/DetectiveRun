import pygame
import random
import const as c
import utility
import vector2

# pylint: disable=no-member
pygame.init()

MINIMUM = c.HEIGHT - 50
OBSTACLE_IMAGES = ["assets/crate.png"]


# obstancle class
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, width, height, velocity):
        super().__init__()
        self.images = OBSTACLE_IMAGES
        imageNum = random.randint(0, len(self.images) - 1)
        self.x = x
        self.bottom = MINIMUM
        self.width = width
        self.height = height
        self.velocity = velocity
        # loading the image
        self.image = pygame.image.load(self.images[imageNum])
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.height = self.image.get_height()
        self.y = self.bottom - self.height
        self.rect.x = self.x
        self.rect.y = self.y

        # saving the history for the quizzes
        self.history = [imageNum]

    def move(self, velocity):
        self.velocity = velocity
        self.x += self.velocity
        self.rect.x = self.x
        self.rect.y = self.y

    def reset(self):
        self.images = ["assets/crate.png"]
        imageNum = random.randint(0, len(self.images) - 1)
        self.image = pygame.image.load(self.images[imageNum])
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.height = self.image.get_height()
        self.x = random.randint(c.WIDTH, c.WIDTH + 100)
        self.y = self.bottom - self.height
        self.history.append(imageNum)


class Player(pygame.sprite.Sprite):
    def __init__(self, x, width, height, gravity):
        super().__init__()
        self.x = x
        self.width = width
        self.height = height * c.FPS_SCALING
        self.gravity = gravity
        self.floor = MINIMUM
        self.yVelocity = 0
        self.jumpPressed = False
        self.faster = 0
        self.points = 0

        image = c.crow.getImage()
        self.image = pygame.transform.scale(image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.y = self.floor - self.height - 5

    def jump(self):
        if self.jumpPressed:
            if self.y < self.floor - self.height:
                self.yVelocity += self.gravity + self.faster
                # appearance
                self.image = c.crow.getImage()

                current_time = pygame.time.get_ticks()
                if current_time - c.crow.last_update >= c.crow.animation_cooldown:
                    c.crow.last_update = current_time

                    if c.crow.frame < 48 or c.crow.frame >= 57:
                        c.crow.frame = 48
                    else:
                        c.crow.frame += 1
            # jump stopping
            else:
                self.yVelocity = 0
                self.y = self.floor - self.height - 5
                # appearance
                self.image = c.crow.getImage()
                current_time = pygame.time.get_ticks()
                if current_time - c.crow.last_update >= c.crow.animation_cooldown:
                    c.crow.last_update = current_time

                    if c.crow.frame < 32 or c.crow.frame >= 41:
                        c.crow.frame = 32
                    else:
                        c.crow.frame += 1

                self.jumpPressed = False
            self.y += self.yVelocity
            self.image = pygame.transform.scale(self.image, (self.width, self.height))

    def move(self):
        self.rect.x = self.x
        self.rect.y = self.y

        self.image = c.crow.getImage()
        current_time = pygame.time.get_ticks()
        if current_time - c.crow.last_update >= c.crow.animation_cooldown:
            c.crow.last_update = current_time

            if c.crow.frame < 32 or c.crow.frame >= 41:
                c.crow.frame = 32
            else:
                c.crow.frame += 1

        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.points += 0.1

    def hasCollided(self, obstacles):
        for obstacle in obstacles:
            if self.rect.colliderect(obstacle.rect):
                return True
        return False

    def displayPoints(self):
        utility.toScreen(
            "Score: " + str(round(self.points)), c.FONT30, c.BLACK, c.WIDTH - 100, 50
        )


class Button:
    def __init__(
        self, x, y, width, height, text, font, colour1, colour2, hasOutline: bool
    ):
        self.rect = None
        self.x = x
        self.y = y

        self.width = width
        self.height = height

        self.text = text
        self.font = font

        self.colours = [colour1, colour2]
        self.colour = colour1
        self.textColour = c.BLACK

        self.hasOutline = hasOutline

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self):
        pygame.draw.rect(c.screen, self.colour, self.rect)

        if self.hasOutline:
            pygame.draw.rect(c.screen, c.BLACK, self.rect, 3)
        if self.is_hovered():
            self.colour = self.colours[1]
        else:
            self.colour = self.colours[0]

        utility.toScreen(
            self.text,
            self.font,
            self.textColour,
            self.x + self.width // 2,
            self.y + self.height // 2,
        )

    def is_hovered(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()

        if self.rect.collidepoint(mouse_x, mouse_y):
            return True

        return False


class QuestionImage(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.images = OBSTACLE_IMAGES
        self.width = width
        self.height = height

        # images
        self.imageNum = random.randint(0, len(self.images) - 1)
        image = pygame.image.load(self.images[self.imageNum])
        self.image = pygame.transform.scale(image, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        # getting the name
        self.imageName = self.images[self.imageNum][:-4] + "s"
        self.imageName = self.imageName[7:]

    def draw(self):
        self.rect.x = self.x
        self.rect.y = self.y


# both the question box and words
class Question:
    def __init__(self, x, y, width, height, history):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = QuestionImage(x, y + 50, width // 3, height // 3)
        self.box = Button(
            x - width // 2,
            y - height // 2,
            width,
            height,
            self.image.imageName,
            c.FONT37,
            c.WHITE,
            c.GRAY,
            True,
        )
        self.answer = history.count(self.image.imageNum)
        self.guess = ""
        self.answerSubmitted = False
        self.correct = False
        self.existing = False

    def draw(self):
        self.existing = True
        self.box.draw()
        self.image.draw()
        utility.toScreen(self.guess, c.FONT30, c.BLUE, self.x, self.y - 50)

    def checkGuess(self):
        if self.answer == self.guess:
            utility.toScreen(
                "You got it right!", c.FONT30, c.GREEN, self.x, self.y - 300
            )
            self.correct = True
        else:
            utility.toScreen2(
                "That wasn't the rhave you passed since the last check?ight answer",
                "The right answer is " + str(self.answer),
                c.FONT30,
                c.RED,
                self.x,
                self.y - 200,
            )

    def getGuess(self, event):
        if self.box.isHovered:
            if event.key == pygame.K_BACKSPACE:
                self.guess[:-1]
            else:
                self.guess += event.unicode

    def checkIfNumber(self):
        numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        numAreDigits = 0
        number = str(self.answer)
        for i in range(0, len(number)):
            for j in range(0, 10):
                if str(number[i]) == str(numbers[j]):
                    numAreDigits += 1
        if numAreDigits == len(number) and len(number) != 0:
            return True
        else:
            return False


class QuestionBox:
    def __init__(self, x, y, width, height, colour):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.colour = colour
        self.rect = (x, y, width, height)

    def draw(self):
        pygame.draw.rect(c.screen, self.colour, self.rect)

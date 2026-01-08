import pygame
import random
import const
import utility
import resources
import vector2
from states.playing import PlayingState

MINIMUM = const.HEIGHT - 50
OBSTACLE_IMAGES = ["assets/crate.png", "assets/Box.png", "assets/Bomb.png"]


# Question stuff
class QuestionImage(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.x = x-140
        self.y = y-140
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
        self.imageName = self.images[self.imageNum][:-4]
        self.imageName = self.imageName[7:]



class Question:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = QuestionImage(x, y + 50, 50, 50)
        self.imageGroup=pygame.sprite.Group()
        self.imageGroup.add(self.image)
        self.box = Button(
            x - width // 2,
            y - height // 2,
            width,
            height,
            self.image.imageName,
            const.FONT37,
            const.WHITE,
            const.GRAY,
            True,
        )

        #dealing with guessing
        self.guess = ""
        self.answerSubmitted = False
        self.correct = True
        self.existing = False
        self.time = 10
        self.obstacleHistory = []

    def draw(self, screen):
        self.existing = True
        self.box.draw(screen)
        self.imageGroup.draw(screen)
        utility.toScreen(
            screen, self.guess, const.FONT30, const.BLUE, self.x, self.y - 50
        )
        self.time -= 1 / const.FPS
        if self.time < -2:
            self.existing = False
            self.reset()
        if self.time > 0:
            utility.toScreen(
                screen,
                "Time left to answer: " + str(round(self.time)),
                const.FONT20,
                const.RED,
                self.x + 50,
                self.y - 80,
            )

    def checkGuess(self):
        self.answer = self.obstacleHistory.count(self.image.imageNum)
        self.answerSubmitted = True
        self.time = 0
        if int(self.answer) == int(self.guess):
            self.correct = True
            return True
        else:
            self.correct = False
            return False

    def getGuess(self, event):
        if self.box.is_hovered:
            if event.key == pygame.K_BACKSPACE:
                self.guess = ""
            elif event.key != pygame.K_SPACE:
                self.guess += event.unicode

    def reset(self):
        self.guess = ""
        self.answerSubmitted = False
        self.correct = True
        self.existing = False
        self.time = 10
        self.obstacleHistory = []

    def checkIfNumber(self):
        numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        numAreDigits = 0
        number = str(self.guess)
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

    def draw(self, screen):
        pygame.draw.rect(screen, self.colour, self.rect)


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, width, height, velocity):
        super().__init__()
        self.images = OBSTACLE_IMAGES
        imageNum = random.randint(0, len(self.images) - 1)
        self.imageNum = imageNum
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
        # question stuff
        self.passedPlayer = False
        self.timesSinceQuestion = 0
        self.time = 0
        self.timeForQuestion = random.randint(3, 6)

    def move(self, velocity, question):
        if not question.existing:
            self.velocity = velocity
            self.x += self.velocity
            self.rect.x = self.x
            self.rect.y = self.y
        else:
            self.timeForQuestion = random.randint(7, 12)

    def hasPassedPlayer(self, player, question: Question):
        if self.x < player.x and not self.passedPlayer:
            self.passedPlayer = True
            # saving the history for the quizzes
            question.obstacleHistory.append(self.imageNum)
            self.timesSinceQuestion += 1

    def askQuestion(self, question: Question):
        if not question.existing:
            if self.timesSinceQuestion == self.timeForQuestion:
                self.time += 1 / const.FPS
                if self.time > 2:
                    question.existing = True

    def reset(self):
        self.images = OBSTACLE_IMAGES
        imageNum = random.randint(0, len(self.images) - 1)
        self.imageNum = imageNum
        self.passedPlayer = False
        self.image = pygame.image.load(self.images[imageNum])
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.height = self.image.get_height()
        self.x = random.randint(const.WIDTH, const.WIDTH + 100)
        self.y = self.bottom - self.height

    def resetQuestion(self):
        self.timesSinceQuestion = 0
        self.time = 10
        self.timeForQuestion = random.randint(0, len(self.images) - 1)


class Player(pygame.sprite.Sprite):
    def __init__(self, x, width, height, gravity, crow_sheet):
        super().__init__()
        self.x = x
        self.width = width
        self.height = height * const.FPS_SCALING
        self.gravity = gravity
        self.floor = MINIMUM + 28
        self.yVelocity = 0
        self.jumpPressed = False
        self.faster = 0
        self.points = 0

        self.crow_sheet = crow_sheet

        image = crow_sheet.get_image()
        self.image = pygame.transform.scale(image, (width, height))
        self.rect = self.image.get_rect()

        self.rect.width = self.width - 30
        self.rect.height = self.height - 30

        self.rect.x = x
        self.y = self.floor - self.height - 5

        self.flying = False
        self.flyingTimer=0

    def jump(self):
        # ... (Same logic as before) ...
        if self.jumpPressed:
            if self.y < self.floor - self.height:
                self.yVelocity += self.gravity + self.faster
                self.image = self.crow_sheet.get_image()
                current_time = pygame.time.get_ticks()
                if (
                    current_time - self.crow_sheet.last_update
                    >= self.crow_sheet.animation_cooldown
                ):
                    self.crow_sheet.last_update = current_time
                    if self.crow_sheet.frame < 48 or self.crow_sheet.frame >= 57:
                        self.crow_sheet.frame = 48
                    else:
                        self.crow_sheet.frame += 1
            else:
                self.yVelocity = 0
                self.y = self.floor - self.height - 5
                self.image = self.crow_sheet.get_image()
                current_time = pygame.time.get_ticks()
                if (
                    current_time - self.crow_sheet.last_update
                    >= self.crow_sheet.animation_cooldown
                ):
                    self.crow_sheet.last_update = current_time
                    if self.crow_sheet.frame < 32 or self.crow_sheet.frame >= 41:
                        self.crow_sheet.frame = 32
                    else:
                        self.crow_sheet.frame += 1
                self.jumpPressed = False
            self.y += self.yVelocity
            self.image = pygame.transform.scale(self.image, (self.width, self.height))

    def move(self, question):
        self.rect.x = self.x
        self.rect.y = self.y
        # ... (Same logic as before) ...
        self.image = self.crow_sheet.get_image()
        current_time = pygame.time.get_ticks()
        if (
            current_time - self.crow_sheet.last_update
            >= self.crow_sheet.animation_cooldown
        ):
            self.crow_sheet.last_update = current_time
            if self.crow_sheet.frame < 32 or self.crow_sheet.frame >= 41:
                self.crow_sheet.frame = 32
            else:
                self.crow_sheet.frame += 1
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        if not question.existing:
            self.points += 0.1

    def hasCollided(self, obstacles):
        for obstacle in obstacles:
            if self.rect.colliderect(obstacle.rect):
                return True
        return False

    def displayPoints(self, screen):  # <--- UPDATED: Takes screen argument
        # NOTE: You must also update utility.toScreen to accept a screen arg!
        utility.toScreen(
            screen,
            "Score: " + str(round(self.points)),
            const.FONT30,
            const.BLACK,
            const.WIDTH - 100,
            50,
        )

    def stopFlying(self):
        if self.flying:
            self.flyingTimer+=1/const.FPS
        if self.flying and self.flyingTimer>5:
            self.flying=False


class Button:
    def __init__(
        self, x, y, width, height, text, font, colour1, colour2, hasOutline: bool
    ):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.font = font
        self.colours = [colour1, colour2]
        self.colour = colour1
        self.textColour = const.BLACK
        self.hasOutline = hasOutline
        self.image = pygame.Surface((self.width, self.height))

        # Check if display is initialized safely
        if pygame.display.get_surface():
            self.image = self.image.convert_alpha()

        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.update_image()

    def update_image(self):
        self.image.fill(self.colour)
        if self.hasOutline:
            pygame.draw.rect(
                self.image, const.BLACK, (0, 0, self.width, self.height), 3
            )
        text_surf = self.font.render(self.text, True, self.textColour)
        text_rect = text_surf.get_rect(center=(self.width // 2, self.height // 2))
        self.image.blit(text_surf, text_rect)

    def draw(self, screen):  # <--- UPDATED: Takes screen argument
        prev_colour = self.colour
        if self.is_hovered():
            self.colour = self.colours[1]
        else:
            self.colour = self.colours[0]

        if prev_colour != self.colour:
            self.update_image()

        # NO MORE CONST.SCREEN
        screen.blit(self.image, self.rect)

    def is_hovered(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        return self.rect.collidepoint(mouse_x, mouse_y)

    def set_alpha(self, alpha):
        self.image.set_alpha(alpha)

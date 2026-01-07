import pygame
import const as c
import resources
import vector2
import utility
from spriteClasses import Player, Obstacle, Question

# pylint: disable=no-member
pygame.init()

# having the obstacles speed up
velocity = -5 * c.FPS_SCALING

# sprites
crow = Player(150, 100, 100, 1 * c.FPS_SCALING)
obstacleSize = 50
obstacle1 = Obstacle(c.WIDTH + 20, obstacleSize, obstacleSize, velocity)
obstacle2 = Obstacle(c.WIDTH + c.WIDTH // 2, obstacleSize, obstacleSize, velocity)
sprites = pygame.sprite.Group()
sprites.add(crow)
sprites.add(obstacle1)
sprites.add(obstacle2)
obstacles = [obstacle1, obstacle2]
tilemap = resources.Resource(
    "assets/Terrain.png",
    vector2.Vector2(32, 32),
    19,
    13,
    0,
    3,
    vector2.Vector2(0, 0),
)


# restarting the variables
def reset():
    global velocity

    for obstacle in obstacles:
        obstacle.reset()
        obstacle.history.clear()
    obstacle2.x += c.WIDTH // 2
    crow.points = 0
    velocity = -5 * c.FPS_SCALING


# dealing with asking questions
history = []

for obstacle in obstacles:
    for num in obstacle.history:
        history.append(num)

question = Question(c.WIDTH // 2, c.HEIGHT // 2, 300, 200, history)


# playing
def render():
    global velocity
    c.screen.fill(c.DARK_GRAY_BLUE)

    tilemap.frame = 21
    tilemap.draw_image(c.screen, vector2.Vector2(0, c.HEIGHT - 70))

    x = 0
    while x < c.WIDTH:
        tilemap.draw_image(c.screen, vector2.Vector2(x, c.HEIGHT - 70))
        x += 32*3

    # moving the crow
    crow.move(question)
    crow.jump()
    crow.displayPoints()

    # obstacles
    for obstacle in obstacles:
        obstacle.move(velocity, question)
        if obstacle.x < -obstacle.width:
            obstacle.reset()
    velocity -= 0.01 * c.FPS_SCALING

    # asking a question
    if question.existing:
        question.draw()
        if question.time<0:
            question.correct=False
        if question.answerSubmitted:
            if question.correct:
                utility.toScreen(
                    "You got it right!", c.FONT30, c.GREEN, question.x, question.y + 150
                )
            else:
                utility.toScreen2(
                    "That wasn't the answer",
                    "The right answer is " + str(question.answer),
                    c.FONT30,
                    c.RED,
                    question.x,
                    question.y + 50,
                )
        if not question.correct:
            utility.toScreen2(
                "You ran out of time.",
                "The right answer is " + str(question.answer),
                c.FONT30,
                c.RED,
                question.x,
                question.y + 50,
            )

    # drawing it
    sprites.draw(c.screen)

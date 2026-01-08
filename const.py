import pygame
import resources
import vector2

pygame.init()

DEV_MODE = False

WIDTH, HEIGHT = 1200, 800
FPS = 60
FPS_SCALING = 30 / FPS

# screen = pygame.display.set_mode((WIDTH, HEIGHT))
# clock = pygame.time.Clock()
pygame.display.set_caption("Detective Run")

# Animation tilemaps
# crow = resources.Resource(
#     "assets/crow-Sheet.png",
#     vector2.Vector2(64, 64),
#     8,
#     14,
#     0,
#     4,
#     vector2.Vector2(0, 0),
# )
# crow.animation_cooldown = 100

# colours
RED = (255, 0, 0)
DARK_RED = (137, 0, 0)
ORANGE = (255, 137, 0)
DARK_ORANGE = (137, 68, 0)
YELLOW = (255, 255, 0)
DARK_YELLOW = (137, 137, 0)
GREEN = (0, 230, 15)
LIGHT_GREEN = (125, 255, 125)
DARK_GREEN = (0, 150, 0)
TEAL = (55, 225, 250)
DARK_TEAL = (0, 137, 137)
BLUE = (0, 0, 255)
DARK_BLUE = (0, 0, 170)
LIGHT_BLUE = (0, 230, 255)
PURPLE = (179, 0, 255)
DARK_PURPLE = (100, 0, 150)
MAGENTA = (255, 0, 255)
DARK_MAGENTA = (137, 0, 137)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (177, 177, 177)
DARK_GRAY = (100, 100, 100)
LIGHT_RED = (255, 91, 91)
DARK_GRAY_BLUE = (57, 56, 82)


# fonts/font sizes
FONT_TYPE = "w.ttf"
FONT10 = pygame.font.Font(FONT_TYPE, 10)
FONT15 = pygame.font.Font(FONT_TYPE, 15)
FONT17 = pygame.font.Font(FONT_TYPE, 17)
FONT20 = pygame.font.Font(FONT_TYPE, 20)
FONT25 = pygame.font.Font(FONT_TYPE, 25)
FONT30 = pygame.font.Font(FONT_TYPE, 30)
FONT37 = pygame.font.Font(FONT_TYPE, 37)
FONT40 = pygame.font.Font(FONT_TYPE, 40)
FONT60 = pygame.font.Font(FONT_TYPE, 60)
FONT200 = pygame.font.Font(FONT_TYPE, 200)

MC_FONT_FILE = "assets/fonts/minecraft/regular"
MC_FONT = pygame.font.Font(MC_FONT_FILE, 30)

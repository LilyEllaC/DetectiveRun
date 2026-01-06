import asyncio

import constants as const
import pygame

import vector2

# pylint: disable=no-member
pygame.init()


# helpful pushing text to screen function
def toScreen(words, font, colour, x, y):
    text = font.render(words, True, colour)
    textRect = text.get_rect()
    textRect.center = (x, y)
    const.screen.blit(text, textRect)


# versions to push more than 1 line
def toScreen2(words1, words2, font, colour, x, y):
    toScreen(words1, font, colour, x, y - font.get_height() // 2)
    toScreen(words2, font, colour, x, y + font.get_height() // 2)


def toScreen3(words1, words2, words3, font, colour, x, y):
    toScreen(words1, font, colour, x, y - font.get_height())
    toScreen(words2, font, colour, x, y)
    toScreen(words3, font, colour, x, y + font.get_height())

async def fadeOutResource(resource):
    for i in range(255, 0, -5):
        await fade(resource, i)

async def fadeInResource(resource):
    for i in range(0, 255, 5):
        await fade(resource, i)

async def fade(resource, alphaValue):
    const.screen.fill((0, 0, 0))
    resource.setAlpha(alphaValue)
    resource.drawImage(const.screen, vector2.Vector2(0, 0))
    pygame.display.flip()
    await asyncio.sleep(0.005)

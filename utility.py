import pygame
import asyncio

import const
import vector2


def toScreen(words, font, colour, x, y):
    text = font.render(words, True, colour)
    textRect = text.get_rect()
    textRect.center = (x, y)

    const.screen.blit(text, textRect)


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


async def fade_to_black():
    snapshot = const.screen.copy()

    overlay = pygame.Surface((const.WIDTH, const.HEIGHT))
    overlay.fill((0, 0, 0))

    for alpha in range(0, 256, 5):
        const.screen.blit(snapshot, (0, 0))

        overlay.set_alpha(alpha)
        const.screen.blit(overlay, (0, 0))

        pygame.display.flip()
        await asyncio.sleep(0.005)


async def fade_from_black():
    snapshot = const.screen.copy()

    overlay = pygame.Surface((const.WIDTH, const.HEIGHT))
    overlay.fill((0, 0, 0))

    for alpha in range(255, -1, -5):
        const.screen.blit(snapshot, (0, 0))

        overlay.set_alpha(alpha)
        const.screen.blit(overlay, (0, 0))

        pygame.display.flip()
        await asyncio.sleep(0.005)


async def fadeInResource(resource):
    for i in range(0, 255, 5):
        await fade(resource, i)


async def fade(resource, alpha_value):
    const.screen.fill((0, 0, 0))

    resource.set_alpha(alpha_value)
    resource.draw_image(const.screen, vector2.Vector2(0, 0))

    pygame.display.flip()

    await asyncio.sleep(0.005)

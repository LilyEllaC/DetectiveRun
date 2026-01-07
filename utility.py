import pygame
import asyncio

import const
import vector2


def toScreen(screen, words, font, colour, x, y):
    text = font.render(words, True, colour)
    textRect = text.get_rect()
    textRect.center = (x, y)

    screen.blit(text, textRect)


def toScreen2(screen, words1, words2, font, colour, x, y):
    toScreen(screen, words1, font, colour, x, y - font.get_height() // 2)
    toScreen(screen, words2, font, colour, x, y + font.get_height() // 2)


def toScreen3(screen, words1, words2, words3, font, colour, x, y):
    toScreen(screen, words1, font, colour, x, y - font.get_height())
    toScreen(screen, words2, font, colour, x, y)
    toScreen(screen, words3, font, colour, x, y + font.get_height())


async def fadeOutResource(resource):
    for i in range(255, 0, -5):
        await fade(resource, i)


async def fade_to_black(screen):
    snapshot = screen.copy()

    overlay = pygame.Surface((const.WIDTH, const.HEIGHT))
    overlay.fill((0, 0, 0))

    for alpha in range(0, 256, 5):
        screen.blit(snapshot, (0, 0))

        overlay.set_alpha(alpha)
        screen.blit(overlay, (0, 0))

        pygame.display.flip()
        await asyncio.sleep(0.005)


async def fade_from_black(screen):
    snapshot = screen.copy()

    overlay = pygame.Surface((const.WIDTH, const.HEIGHT))
    overlay.fill((0, 0, 0))

    for alpha in range(255, -1, -5):
        screen.blit(snapshot, (0, 0))

        overlay.set_alpha(alpha)
        screen.blit(overlay, (0, 0))

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

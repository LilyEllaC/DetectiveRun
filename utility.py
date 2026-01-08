import pygame
import asyncio
import colorsys
import os

import const
import vector2

loaded_fonts = {}


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


# highScore stuff
# getting from and pushing to files
def getFromFile(fileName):
    with open(fileName, "r") as file:
        highScore = file.read()
    return highScore


# push name to file
def pushToFile(score, fileName):
    with open(fileName, "w") as file:
        file.write(str(score))


def toScreen(screen, words, font, colour, x, y):
    text = font.render(words, True, colour)
    textRect = text.get_rect()
    textRect.center = (x, y)

    screen.blit(text, textRect)


def get_font(font, font_size, is_bold=False, is_italic=False):
    target_font = None
    key = f"{font}.{font_size}.{is_bold}.{is_italic}"

    if key in loaded_fonts:
        target_font = loaded_fonts[key]

    if target_font is None:
        base_path = f"assets/fonts/{font}"

        if os.path.isdir(base_path):
            if is_bold and is_italic:
                filename = "bold-italic"
            elif is_bold:
                filename = "bold"
            elif is_italic:
                filename = "italic"
            else:
                filename = "regular"

            font_path = os.path.join(base_path, filename)
        else:
            font_path = base_path

        try:
            target_font = pygame.font.Font(font_path, font_size)
        except FileNotFoundError:
            print(
                f"Warning: Could not find font {font_path}. Falling back to default styling."
            )

            if os.path.isdir(base_path):
                fallback_path = os.path.join(base_path, "regular")

                try:
                    target_font = pygame.font.Font(fallback_path, font_size)
                    target_font.set_bold(is_bold)
                    target_font.set_italic(is_italic)
                except FileNotFoundError:
                    target_font = pygame.font.Font(None, font_size)
            else:
                target_font = pygame.font.Font(base_path, font_size)
                target_font.set_bold(is_bold)
                target_font.set_italic(is_italic)

        loaded_fonts[key] = target_font

    return target_font


def to_screen(
    screen, words, font, font_size, colour, x, y, is_bold=False, is_italic=False
):
    if isinstance(words, str):
        words = [words]

    target_font = get_font(font, font_size, is_bold, is_italic)

    idx = 0
    line_height = 2
    height = len(words) * (target_font.get_height() + line_height)

    for word in words:
        new_y = y + ((target_font.get_height() + line_height // 2) * idx)

        text = target_font.render(word, True, colour)
        text_rect = text.get_rect()
        text_rect.center = (x, new_y)

        screen.blit(text, text_rect)

        idx += 1

    return {"height": height}


def draw_centered_pair(
    screen,
    label_text,
    value_text,
    font_name,
    font_size,
    label_color,
    value_color,
    center_x,
    center_y,
    spacing=10,
    is_bold=False,
):
    target_font = get_font(font_name, font_size, is_bold=is_bold)

    label_surf = target_font.render(label_text, True, label_color)
    value_surf = target_font.render(str(value_text), True, value_color)

    total_width = label_surf.get_width() + spacing + value_surf.get_width()
    start_x = center_x - (total_width // 2)

    # Use center_y for vertical centering
    # to_screen uses "center" of rect, but iterates lines.
    # Here we just assume single line.

    # We want center_y to be the middle of the text height
    max_height = max(label_surf.get_height(), value_surf.get_height())

    label_rect = label_surf.get_rect(midleft=(start_x, center_y))
    value_rect = value_surf.get_rect(midleft=(label_rect.right + spacing, center_y))

    screen.blit(label_surf, label_rect)
    screen.blit(value_surf, value_rect)

    return {"height": max_height}


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


def lerp(color_a, color_b, value_a, value_b):
    try:
        val_a = float(value_a)
        val_b = float(value_b)
    except ValueError:
        return color_a

    if val_b == 0:
        t = 0.0
    else:
        t = val_a / val_b

    t = max(0.0, min(1.0, t))

    r1, g1, b1 = [x / 255.0 for x in color_a]
    r2, g2, b2 = [x / 255.0 for x in color_b]

    h1, s1, v1 = colorsys.rgb_to_hsv(r1, g1, b1)
    h2, s2, v2 = colorsys.rgb_to_hsv(r2, g2, b2)

    dist = h2 - h1
    if h1 > h2 and abs(dist) > 0.5:
        h1 -= 1
    elif h2 > h1 and abs(dist) > 0.5:
        h2 -= 1

    h = h1 + (h2 - h1) * t
    h %= 1.0
    s = s1 + (s2 - s1) * t
    v = v1 + (v2 - v1) * t

    r, g, b = colorsys.hsv_to_rgb(h, s, v)
    return (int(r * 255), int(g * 255), int(b * 255))

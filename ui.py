import pygame
import re
import io
import random
import const
import utility
import resources
import vector2
from states.playing import PlayingState

MINIMUM = const.HEIGHT - 50
obstacleImages = ["assets/crate.png", "assets/Box.png", "assets/Bomb.png"]


# Question stuff
class QuestionImage(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.x = x - 140
        self.y = y - 140
        self.images = obstacleImages
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
        self.imageGroup = pygame.sprite.Group()
        self.imageGroup.add(self.image)
        self.box = Button()
        self.box.text = self.image.imageName
        self.box.x = x - width // 2
        self.box.y = y - height // 2
        self.box.width = width
        self.box.height = height
        self.box.font_size = 37
        self.box.colour = const.WHITE
        self.box.hover_colour = const.GRAY
        self.box.has_outline = True
        self.box.border_radius = 10

        # dealing with guessing
        # self.guess = ""
        # self.answerSubmitted = False
        # self.correct = True
        # self.existing = False
        # self.time = 10
        # self.obstacleHistory = []

        self.reset()

    def reset(self):
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
        if self.box.is_hovered():
            if event.key == pygame.K_BACKSPACE:
                self.guess = ""
            elif event.key != pygame.K_SPACE:
                self.guess += event.unicode

    def checkIfNumber(self):
        try:
            int(self.guess)
            return True
        except ValueError:
            return False

        # numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        # numAreDigits = 0
        # number = str(self.guess)
        # for i in range(0, len(number)):
        #     for j in range(0, 10):
        #         if str(number[i]) == str(numbers[j]):
        #             numAreDigits += 1
        # if numAreDigits == len(number) and len(number) != 0:
        #     return True
        # else:
        #     return False


# class QuestionBox:
#     def __init__(self, x, y, width, height, colour):
#         self.x = x
#         self.y = y
#         self.width = width
#         self.height = height
#         self.colour = colour
#         self.rect = (x, y, width, height)

#     def draw(self, screen):
#         pygame.draw.rect(screen, self.colour, self.rect)


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, width, height, velocity):
        super().__init__()
        self.images = obstacleImages
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
            self.timeForQuestion = random.randint(3, 6)

    def hasPassedPlayer(self, player, question: Question):
        if self.x < player.x and not self.passedPlayer:
            print(self.timesSinceQuestion, self.timeForQuestion)
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
        self.images = obstacleImages
        imageNum = random.randint(0, len(self.images) - 1)
        self.imageNum = imageNum
        self.passedPlayer = False
        self.image = pygame.image.load(self.images[imageNum])
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.height = self.image.get_height()
        self.x = random.randint(const.WIDTH, const.WIDTH + 100)
        self.y = self.bottom - self.height
        self.rect.x = self.x
        self.rect.y = self.y

    def resetQuestion(self):
        self.timesSinceQuestion = 0
        self.time = 10
        self.timeForQuestion = random.randint(0, len(self.images) - 1)


class Player(pygame.sprite.Sprite):
    def __init__(self, x, width, height, gravity, crow_sheet):
        super().__init__()
        self.x = x
        self.width = width
        self.height = height
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
        self.flyingTimer = 0

    def jump(self):
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
            self.points += 0.1*const.FPS_SCALING

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
            self.flyingTimer += 1 / const.FPS
        if self.flying and self.flyingTimer > 7:
            self.flying = False


class Button:
    def __init__(self):
        self._text = ""
        self._x = 0
        self._y = 0
        self._width = 200
        self._height = 50
        self._font_name = "minecraft"
        self._font_size = 20

        # Colors
        self._colour = (255, 255, 255)  # Default normal color
        self._hover_colour = (200, 200, 200)  # Default hover color
        self._text_colour = const.BLACK
        self._border_colour = const.BLACK

        # Style
        self._has_outline = False
        self._border_radius = 0
        self._border_width = 3
        self._anchor_point = (0, 0)

        self.rect = pygame.Rect(self._x, self._y, self._width, self._height)
        self.font = None
        self._update_font()

        # Cache surface
        self.image = None
        self._needs_redraw = True

    def _update_font(self):
        self.font = utility.get_font(self._font_name, self._font_size)
        self._needs_redraw = True

    def _update_rect(self):
        self.rect = pygame.Rect(self._x, self._y, self._width, self._height)
        # Apply anchor point
        self.rect.x = self._x - int(self._width * self._anchor_point[0])
        self.rect.y = self._y - int(self._height * self._anchor_point[1])
        self._needs_redraw = True

    # --- Properties ---

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        if self._text != value:
            self._text = value
            self._needs_redraw = True

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        if self._x != value:
            self._x = value
            self._update_rect()

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        if self._y != value:
            self._y = value
            self._update_rect()

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        if self._width != value:
            self._width = value
            self._update_rect()

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        if self._height != value:
            self._height = value
            self._update_rect()

    @property
    def colour(self):
        return self._colour

    @colour.setter
    def colour(self, value):
        self._colour = value
        self._needs_redraw = True

    @property
    def hover_colour(self):
        return self._hover_colour

    @hover_colour.setter
    def hover_colour(self, value):
        self._hover_colour = value

    @property
    def text_colour(self):
        return self._text_colour

    @text_colour.setter
    def text_colour(self, value):
        self._text_colour = value
        self._needs_redraw = True

    @property
    def border_colour(self):
        return self._border_colour

    @border_colour.setter
    def border_colour(self, value):
        self._border_colour = value
        self._needs_redraw = True

    @property
    def has_outline(self):
        return self._has_outline

    @has_outline.setter
    def has_outline(self, value):
        self._has_outline = value
        self._needs_redraw = True

    @property
    def border_radius(self):
        return self._border_radius

    @border_radius.setter
    def border_radius(self, value):
        self._border_radius = value
        self._needs_redraw = True

    @property
    def font_size(self):
        return self._font_size

    @font_size.setter
    def font_size(self, value):
        self._font_size = value
        self._update_font()

    @property
    def anchor_point(self):
        return self._anchor_point

    @anchor_point.setter
    def anchor_point(self, value):
        self._anchor_point = value
        self._update_rect()

    def is_hovered(self, mouse_pos=None):
        if mouse_pos is None:
            mouse_pos = pygame.mouse.get_pos()
        return self.rect.collidepoint(mouse_pos)

    def _redraw(self, current_colour):
        self.image = pygame.Surface((self._width, self._height), pygame.SRCALPHA)

        # Draw background
        pygame.draw.rect(
            self.image,
            current_colour,
            (0, 0, self._width, self._height),
            border_radius=self._border_radius,
        )

        # Draw outline
        if self._has_outline:
            pygame.draw.rect(
                self.image,
                self._border_colour,
                (0, 0, self._width, self._height),
                self._border_width,
                border_radius=self._border_radius,
            )

        # Draw text
        if self.font and self._text:
            text_surf = self.font.render(self._text, True, self._text_colour)
            text_rect = text_surf.get_rect(center=(self._width // 2, self._height // 2))
            self.image.blit(text_surf, text_rect)

    def draw(self, screen, mouse_pos=None):
        current_colour = (
            self._hover_colour if self.is_hovered(mouse_pos) else self._colour
        )

        # We redrawing every frame essentially because color changes on hover
        # But we can optimize to only redraw if state changes.
        # For simplicity and correctness with hover, let's redraw on the fly or cache 2 states.
        # simpler: just draw directly to screen or update cached image if needed.

        self._redraw(current_colour)
        screen.blit(self.image, self.rect.topleft)


class Label:
    def __init__(self):
        # Initialize private variables
        self._text = [""]
        self._font_name = "minecraft"
        self._font_size = 20
        self._colour = (255, 255, 255)
        self._x = 0
        self._y = 0
        self._anchor_point = (0, 0)
        self._is_bold = False
        self._is_italic = False
        self.underline_on_hover = False

        self.line_height = 2
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.font = None

        # Initial build
        self._update_font()

    def _update_font(self):
        self.font = utility.get_font(
            self._font_name, self._font_size, self._is_bold, self._is_italic
        )
        self.update_rect()

    def update_rect(self):
        if not self.font:
            return

        font_h = self.font.get_height()
        total_h = len(self._text) * (font_h + self.line_height)

        max_w = 0
        for line in self._text:
            w, h = self.font.size(line)
            if w > max_w:
                max_w = w

        self.rect.width = max_w
        self.rect.height = total_h

        self.rect.x = self._x - int(self.rect.width * self._anchor_point[0])
        self.rect.y = self._y - int(self.rect.height * self._anchor_point[1])

    # --- Properties ---

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text = value if not isinstance(value, str) else [value]
        self.update_rect()

    @property
    def font_name(self):
        return self._font_name

    @font_name.setter
    def font_name(self, value):
        self._font_name = value
        self._update_font()

    @property
    def font_size(self):
        return self._font_size

    @font_size.setter
    def font_size(self, value):
        self._font_size = value
        self._update_font()

    @property
    def colour(self):
        return self._colour

    @colour.setter
    def colour(self, value):
        self._colour = value

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value
        self.update_rect()

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value
        self.update_rect()

    @property
    def is_bold(self):
        return self._is_bold

    @is_bold.setter
    def is_bold(self, value):
        self._is_bold = value
        self._update_font()

    @property
    def is_italic(self):
        return self._is_italic

    @is_italic.setter
    def is_italic(self, value):
        self._is_italic = value
        self._update_font()

    @property
    def width(self):
        return self.rect.width

    @property
    def height(self):
        return self.rect.height

    @property
    def anchor_point(self):
        return self._anchor_point

    @anchor_point.setter
    def anchor_point(self, value):
        self._anchor_point = value
        self.update_rect()

    def draw(self, screen, mouse_pos=None):
        idx = 0
        is_hovered = self.is_hovered(mouse_pos)

        for line in self._text:
            new_y = self._y + ((self.font.get_height() + self.line_height // 2) * idx)

            text_surf = self.font.render(line, True, self._colour)
            text_rect = text_surf.get_rect()

            # Re-calculate position based on wrapped lines if we were supporting wrapping,
            # but currently we just list lines.
            # We must respect the rect position which is already offset by anchor.
            # Wait, the logic below 'new_y' uses self._y which is not the top-left of the rect?
            # Actually, self._y is the position of the anchor.
            # So we need to calculate drawing position based on self.rect.

            # Correct drawing logic:
            # We want to draw relative to self.rect.x, self.rect.y
            # The Label handles multiline by just stacking.

            draw_x = self.rect.x
            draw_y = self.rect.y + (
                (self.font.get_height() + self.line_height // 2) * idx
            )

            text_rect.topleft = (draw_x, draw_y)
            screen.blit(text_surf, text_rect)

            if self.underline_on_hover and is_hovered:
                # elegant underline 2px below text, 2px thick
                start_pos = (text_rect.left, text_rect.bottom - 2)
                end_pos = (text_rect.right, text_rect.bottom - 2)
                pygame.draw.line(screen, self._colour, start_pos, end_pos, 2)

            idx += 1

    def is_hovered(self, mouse_pos=None):
        if mouse_pos is None:
            mouse_pos = pygame.mouse.get_pos()
        return self.rect.collidepoint(mouse_pos)


class Icon:
    def __init__(self, path):
        self._path = path
        self._x = 0
        self._y = 0
        self._width = 32
        self._height = 32
        self._anchor_point = (0, 0)
        self._width = 32
        self._height = 32
        self._colour = None  # None = original color
        self.image = None
        self._reload_image()

    def _reload_image(self):
        try:
            if self._path.endswith(".svg"):
                # Load SVG with specific dimensions to avoid pixelation
                with open(self._path, "r") as f:
                    content = f.read()

                # Regex to find the opening <svg ...> tag
                svg_tag_match = re.search(r"<svg[^>]*>", content)
                if svg_tag_match:
                    tag_content = svg_tag_match.group(0)

                    # Update or add width
                    if 'width="' in tag_content:
                        tag_content = re.sub(
                            r'(?<!-)width="[^"]*"',
                            f'width="{self._width}"',
                            tag_content,
                        )
                    else:
                        tag_content = tag_content.replace(
                            "<svg", f'<svg width="{self._width}"'
                        )

                    # Update or add height
                    if 'height="' in tag_content:
                        tag_content = re.sub(
                            r'(?<!-)height="[^"]*"',
                            f'height="{self._height}"',
                            tag_content,
                        )
                    else:
                        tag_content = tag_content.replace(
                            "<svg", f'<svg height="{self._height}"'
                        )

                    content = content.replace(svg_tag_match.group(0), tag_content)

                bio = io.BytesIO(content.encode("utf-8"))
                self.image = pygame.image.load(bio, "icon.svg").convert_alpha()
            else:
                self.image = pygame.image.load(self._path).convert_alpha()

            self.image = pygame.transform.scale(self.image, (self._width, self._height))
            # Apply anchor
            r_x = self._x - int(self._width * self._anchor_point[0])
            r_y = self._y - int(self._height * self._anchor_point[1])
            self.rect = self.image.get_rect(topleft=(r_x, r_y))
            if self._colour:
                # Create a silhouette with white color and original alpha
                # We use BLEND_RGBA_MAX to force RGB to 255 (white) while keeping Alpha unchanged (max(A, 0) = A)
                silhouette = self.image.copy()
                silhouette.fill((255, 255, 255, 0), special_flags=pygame.BLEND_RGBA_MAX)

                # Create a solid color surface
                color_surface = pygame.Surface(self.image.get_size(), pygame.SRCALPHA)
                color_surface.fill(self._colour)

                # Multiply solid color by silhouette
                # (R_dst * 1, G_dst * 1, B_dst * 1, 255 * A_src) -> (R_dst, G_dst, B_dst, A_src)
                color_surface.blit(
                    silhouette, (0, 0), special_flags=pygame.BLEND_RGBA_MULT
                )

                self.image = color_surface
        except Exception as e:
            print(f"Error loading icon {self._path}: {e}")
            self.image = pygame.Surface((self._width, self._height))
            self.image.fill((255, 0, 255))  # Error magenta
            r_x = self._x - int(self._width * self._anchor_point[0])
            r_y = self._y - int(self._height * self._anchor_point[1])
            self.rect = self.image.get_rect(topleft=(r_x, r_y))

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, value):
        self._path = value
        self._reload_image()

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value
        self.rect.x = int(self._x - (self._width * self._anchor_point[0]))

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value
        self.rect.y = int(self._y - (self._height * self._anchor_point[1]))

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        self._width = value
        self._reload_image()

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        self._height = value
        self._reload_image()

    @property
    def colour(self):
        return self._colour

    @colour.setter
    def colour(self, v):
        self._colour = v
        self._reload_image()

    @property
    def anchor_point(self):
        return self._anchor_point

    @anchor_point.setter
    def anchor_point(self, value):
        self._anchor_point = value
        # Update rect position without reloading image if possible,
        # but _reload_image does the rect init.
        # Efficient way: just update rect.
        r_x = self._x - int(self._width * self._anchor_point[0])
        r_y = self._y - int(self._height * self._anchor_point[1])
        self.rect.topleft = (r_x, r_y)

    def draw(self, screen, mouse_pos=None):
        if self.image:
            screen.blit(self.image, self.rect.topleft)


class Frame:
    def __init__(self):
        self._x = 0
        self._y = 0
        self._width = 100
        self._height = 100
        self._background_colour = None  # None means transparent
        self._border_colour = (255, 255, 255)
        self._border_radius = 0
        self._border_width = 0
        self.children = []
        self._surface = None
        self._needs_redraw = True
        self.rect = pygame.Rect(self._x, self._y, self._width, self._height)

        # Layout properties
        self._layout = None  # None, 'vertical', 'horizontal'
        self._gap = 0
        self._cross_align = "center"  # 'start', 'center'

    def is_hovered(self, mouse_pos=None):
        if mouse_pos is None:
            mouse_pos = pygame.mouse.get_pos()
        # Since Frame is blitted to screen at self._x, self._y,
        # its rect should be in screen coordinates.
        # Ensure rect is updated when x/y/w/h change.
        return self.rect.collidepoint(mouse_pos)

    def add_child(self, child):
        self.children.append(child)
        self._reflow()
        self._needs_redraw = True

    def _reflow(self):
        if not self._layout:
            return

        current_x = 0
        current_y = 0

        # For centering logic, we might need to know max width/height of children
        # But simple stacking is first priority.

        if self._layout == "vertical":
            for child in self.children:
                # Center horizontally if requested
                if self._cross_align == "center":
                    child.x = (self._width - child.width) // 2
                else:
                    child.x = 0  # Start

                child.y = current_y
                current_y += child.height + self._gap

        elif self._layout == "horizontal":
            # For horizontal, we might want to vertically center items
            # This requires knowing the row height, or just centering in Frame height?
            # Let's align relative to Frame height for now if cross_align is center

            for child in self.children:
                child.x = current_x
                current_x += child.width + self._gap

                if self._cross_align == "center":
                    child.y = (self._height - child.height) // 2
                else:
                    child.y = 0

    @property
    def layout(self):
        return self._layout

    @layout.setter
    def layout(self, v):
        self._layout = v
        self._reflow()
        self._needs_redraw = True

    @property
    def gap(self):
        return self._gap

    @gap.setter
    def gap(self, v):
        self._gap = v
        self._reflow()
        self._needs_redraw = True

    @property
    def cross_align(self):
        return self._cross_align

    @cross_align.setter
    def cross_align(self, v):
        self._cross_align = v
        self._reflow()
        self._needs_redraw = True

    def _redraw(self):
        self._surface = pygame.Surface((self._width, self._height), pygame.SRCALPHA)

        if self._background_colour:
            pygame.draw.rect(
                self._surface,
                self._background_colour,
                (0, 0, self._width, self._height),
                border_radius=self._border_radius,
            )

        if self._border_width > 0:
            pygame.draw.rect(
                self._surface,
                self._border_colour,
                (0, 0, self._width, self._height),
                self._border_width,
                border_radius=self._border_radius,
            )
        self._needs_redraw = False

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, v):
        self._x = v
        self.rect.x = v
        self._needs_redraw = True

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, v):
        self._y = v
        self.rect.y = v
        self._needs_redraw = True

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, v):
        self._width = v
        self.rect.width = v
        self._needs_redraw = True

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, v):
        self._height = v
        self.rect.height = v
        self._needs_redraw = True

    @property
    def background_colour(self):
        return self._background_colour

    @background_colour.setter
    def background_colour(self, v):
        self._background_colour = v
        self._needs_redraw = True

    @property
    def border_colour(self):
        return self._border_colour

    @border_colour.setter
    def border_colour(self, v):
        self._border_colour = v
        self._needs_redraw = True

    @property
    def border_radius(self):
        return self._border_radius

    @border_radius.setter
    def border_radius(self, v):
        self._border_radius = v
        self._needs_redraw = True

    @property
    def border_width(self):
        return self._border_width

    @border_width.setter
    def border_width(self, v):
        self._border_width = v
        self._needs_redraw = True

    def draw(self, screen, mouse_pos=None):
        # 1. Prepare base frame surface
        if self._needs_redraw or not self._surface:
            self._redraw()

        if mouse_pos is None:
            mouse_pos = pygame.mouse.get_pos()

        # Create a copy or clear it?
        # If children are dynamic, we need to fresh start from the cached background.
        final_surf = self._surface.copy()

        # Transform mouse pos for children
        # Children are drawn on final_surf at (0,0) offset from frame
        # So child_mouse_x = mouse_x - frame_x
        # BUT: self._x and self._y are where the frame is drawn on SCREEN (or parent surface)
        # So we subtract them from current mouse_pos to get local pos.
        child_mouse_pos = (mouse_pos[0] - self._x, mouse_pos[1] - self._y)

        # 2. Draw children onto this surface
        for child in self.children:
            # We check if child accepts mouse_pos arg (it should if it's UI)
            # Use simple try/except or just assume API compliance if we control all widgets
            try:
                child.draw(final_surf, mouse_pos=child_mouse_pos)
            except TypeError:
                child.draw(final_surf)

        # 3. Blit to main screen
        screen.blit(final_surf, (self._x, self._y))


class Spritesheet:
    def __init__(self, filename):
        try:
            self.sheet = pygame.image.load(filename).convert_alpha()
        except Exception as e:
            print(f"Unable to load spritesheet image: {filename}")
            raise e

        self._frame_width = 1
        self._frame_height = 1
        self._total_frames = 1
        self._columns = 1
        self._scale = 1

        self.frames = []
        self.animations = {}
        self.current_animation = None
        self.current_frame_index = 0
        self.timer = 0
        self.image = None

    def _split_sheet(self):
        self.frames = []
        if self._frame_width == 0 or self._frame_height == 0:
            return

        for i in range(self._total_frames):
            x = (i % self._columns) * self._frame_width
            y = (i // self._columns) * self._frame_height

            # Bounds check
            if (
                x + self._frame_width > self.sheet.get_width()
                or y + self._frame_height > self.sheet.get_height()
            ):
                continue

            rect = pygame.Rect(x, y, self._frame_width, self._frame_height)
            frame = self.sheet.subsurface(rect)

            if self._scale != 1:
                frame = pygame.transform.scale(
                    frame,
                    (
                        int(self._frame_width * self._scale),
                        int(self._frame_height * self._scale),
                    ),
                )

            self.frames.append(frame)

        if self.frames:
            self.image = self.frames[0]

    def _update_dimensions(self):
        if self._frame_width > 0 and self._frame_height > 0:
            sheet_width = self.sheet.get_width()
            sheet_height = self.sheet.get_height()
            self._columns = sheet_width // self._frame_width
            rows = sheet_height // self._frame_height
            self._total_frames = self._columns * rows
            self._split_sheet()

    @property
    def frame_width(self):
        return self._frame_width

    @frame_width.setter
    def frame_width(self, value):
        self._frame_width = value
        self._update_dimensions()

    @property
    def frame_height(self):
        return self._frame_height

    @frame_height.setter
    def frame_height(self, value):
        self._frame_height = value
        self._update_dimensions()

    # total_frames and columns are now read-only properties inferred from sheet
    @property
    def total_frames(self):
        return self._total_frames

    @property
    def columns(self):
        return self._columns

    @property
    def scale(self):
        return self._scale

    @scale.setter
    def scale(self, value):
        self._scale = value
        self._split_sheet()

    # --- Animation Methods ---

    def add_animation(
        self, name, start_frame, end_frame, time_between_frames, loop=True
    ):
        self.animations[name] = {
            "frames": list(range(start_frame, end_frame + 1)),
            "speed": time_between_frames,
            "loop": loop,
        }

    def play(self, name):
        if self.current_animation != name:
            self.current_animation = name
            self.current_frame_index = 0
            self.timer = pygame.time.get_ticks()
            self.update_image()

    def update(self):
        if self.current_animation and self.frames:
            anim = self.animations[self.current_animation]
            if pygame.time.get_ticks() - self.timer >= anim["speed"]:
                self.timer = pygame.time.get_ticks()

                if anim["loop"]:
                    self.current_frame_index = (self.current_frame_index + 1) % len(
                        anim["frames"]
                    )
                else:
                    if self.current_frame_index < len(anim["frames"]) - 1:
                        self.current_frame_index += 1

                self.update_image()

    def update_image(self):
        if self.current_animation and self.frames:
            anim = self.animations[self.current_animation]
            # Safety check for index
            if self.current_frame_index < len(anim["frames"]):
                frame_idx = anim["frames"][self.current_frame_index]
                if frame_idx < len(self.frames):
                    self.image = self.frames[frame_idx]

    def draw(self, screen, x, y):
        if self.image:
            screen.blit(self.image, (x, y))

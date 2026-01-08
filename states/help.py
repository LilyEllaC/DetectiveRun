import pygame
import resources
import ui
import const
import utility as utils
import vector2

from states.base import GameState


class HelpState(GameState):
    def __init__(self, manager):
        super().__init__(manager)

        self.bg = resources.Resource(
            "assets/help.png",
            vector2.Vector2(2304, 1296),
            1,
            1,
            1,
            0.7,
            vector2.Vector2(0, 0),
        )

        self.overlay = pygame.Surface(
            (const.WIDTH - 82, const.HEIGHT - 82), pygame.SRCALPHA
        )

        self.keysLetterAndSymbols = resources.Resource(
            "assets/Keyboard Letters and Symbols.png",
            vector2.Vector2(16, 16),
            8,
            14,
            1,
            3,
            vector2.Vector2(0, 0),
        )

        self.keysExtra = resources.Resource(
            "assets/Keyboard Extras.png",
            vector2.Vector2(16, 16),
            8,
            8,
            20,
            3,
            vector2.Vector2(0, 0),
        )

        self.font = "minecraft"

        self.back_label = ui.Label()
        self.back_label.text = "< Back"
        self.back_label.font_name = self.font
        self.back_label.font_size = 24
        self.back_label.colour = const.WHITE
        self.back_label.x = 96
        self.back_label.y = 74
        self.back_label.is_italic = True
        self.back_label.underline_on_hover = True

    def on_enter(self, **kwargs):
        print("--- Entering Help ---")

        for key, value in kwargs.items():
            setattr(self, key, value)

    async def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.back_label.is_hovered():
                    await utils.fade_to_black(self.manager.screen)

                    await self.manager.change_state("INTRO")

                    # await utils.fade_from_black(self.manager.screen)

    def draw(self, screen):
        self.bg.draw_image(screen, vector2.Vector2(0, 0))

        pygame.draw.rect(
            self.overlay, (0, 0, 0, 150), self.overlay.get_rect(), border_radius=25
        )

        overlay_x = (const.WIDTH - self.overlay.get_width()) // 2
        overlay_y = (const.HEIGHT - self.overlay.get_height()) // 2
        screen.blit(self.overlay, (overlay_x, overlay_y))

        text_base_y = 100

        text_base_y += utils.to_screen(
            screen,
            ["How to play?"],
            self.font,
            40,
            const.WHITE,
            const.WIDTH / 2,
            text_base_y,
            is_bold=True,
        )["height"]

        text_base_y += 24

        text_base_y += utils.to_screen(
            screen,
            [
                "After uncovering the murderer's identity, you begin the chase.",
                "",
                "Stay focused: while pursuing him, your colleagues will question you",
                "to gather crucial information about what obstacles he is using to block his path.",
                "",
                "Crashing into an obstacle will prove the end of the journey.",
            ],
            self.font,
            20,
            const.WHITE,
            const.WIDTH / 2,
            text_base_y,
        )["height"]

        text_base_y += 32

        text_base_y += utils.to_screen(
            screen,
            ["Controls"],
            self.font,
            30,
            const.WHITE,
            const.WIDTH / 2,
            text_base_y,
        )["height"]

        text_base_y += 8

        self.keysLetterAndSymbols.draw_image(
            screen, vector2.Vector2(const.WIDTH / 2 - 72, text_base_y)
        )

        utils.to_screen(
            screen,
            ["Jump"],
            self.font,
            20,
            const.WHITE,
            const.WIDTH / 2 + 48,
            text_base_y + 22,
            is_italic=True,
        )

        text_base_y += 45
        self.keysExtra.frame = 20
        self.keysExtra.draw_image(
            screen, vector2.Vector2(const.WIDTH / 2 - 96, text_base_y)
        )
        self.keysExtra.frame = 21
        self.keysExtra.draw_image(
            screen, vector2.Vector2(const.WIDTH / 2 - 48, text_base_y)
        )

        utils.to_screen(
            screen,
            ["Fall"],
            self.font,
            20,
            const.WHITE,
            const.WIDTH / 2 + 48,
            text_base_y + 22,
            is_italic=True,
        )

        text_base_y += 100

        text_base_y += utils.to_screen(
            screen,
            [
                "When a boxed word appears in the screen, this is a colleague",
                "asking how many of those objects you have jumped over since the last message.",
                "",
                "To reply, enter the number by hovering over the box, typing the number and clicking",
                "",
                "If you enter the correct number, the obstacles will slow down",
                "and you will be given the temporary ability to fly",
                "",
                "If you got the question wrong, obstacles will speed up",
            ],
            self.font,
            20,
            const.WHITE,
            const.WIDTH / 2,
            text_base_y,
        )["height"]

        # pygame.draw.line(screen, const.WHITE, (89, 59), (49, 59), 4)
        # pygame.draw.line(screen, const.WHITE, (49, 59), (69, 69), 4)
        # pygame.draw.line(screen, const.WHITE, (49, 59), (69, 49), 4)

        self.back_label.draw(screen)

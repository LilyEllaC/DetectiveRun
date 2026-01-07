import pygame
import resources
import ui
import const
import utility
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

        self.back_button = ui.Button(
            38, 30, 50, 50, "", const.FONT40, (0, 0, 0, 0), (0, 0, 0, 0), False
        )

    def on_enter(self, **kwargs):
        print("--- Entering Help ---")

        for key, value in kwargs.items():
            setattr(self, key, value)

    async def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.back_button.is_hovered():
                    await utility.fade_to_black(self.manager.screen)

                    await self.manager.change_state("INTRO")

                    # await utility.fade_from_black(self.manager.screen)

    def draw(self, screen):
        self.bg.draw_image(screen, vector2.Vector2(0, 0))

        utility.toScreen(
            screen, "How to play?", const.FONT60, const.BLACK, const.WIDTH / 2, 100
        )

        utility.toScreen3(
            screen,
            "After uncovering the murderer’s identity, you begin the chase.",
            "Stay focused: while pursuing him, your colleagues will question you to gather crucial information about what obstacles he is using to block his path.",
            "Crashing into an obstacle will prove the end of the journey.",
            const.FONT20,
            const.BLACK,
            const.WIDTH / 2,
            200,
        )
        utility.toScreen3(
            screen,
            "When a boxed word appears in the screen, this is a colleague asking how many of those objects you have jumped over since the last message.",
            "To reply, enter the number by hovering over the box, typing the number and clicking",
            "If you enter the correct number, the obstacles will slow and you will be given the temporary ability to fly",
            const.FONT20,
            const.WHITE,
            const.WIDTH / 2,
            700,
        )
        utility.toScreen(
            screen,
            "However, if you enter the wrong number or are too slow responding, the obstacles will increase in speed",
            const.FONT20,
            const.WHITE,
            const.WIDTH / 2,
            750,
        )

        utility.toScreen(
            screen, "Controls", const.FONT30, const.BLACK, const.WIDTH / 2, 290
        )

        self.keysLetterAndSymbols.draw_image(screen, vector2.Vector2(const.WIDTH / 2 - 72, 400))

        self.keysExtra.frame = 20
        self.keysExtra.draw_image(screen, vector2.Vector2(const.WIDTH / 2 - 96, 365))
        self.keysExtra.frame = 21
        self.keysExtra.draw_image(screen, vector2.Vector2(const.WIDTH / 2 - 48, 365))

        utility.toScreen(
            screen,
            "Fall",
            const.FONT20,
            const.BLACK,
            const.WIDTH / 2 + 48,
            380,
        )

        utility.toScreen(
            screen,
            "Jump",
            const.FONT20,
            const.BLACK,
            const.WIDTH / 2 + 48,
            420,
        )

        pygame.draw.line(screen, const.BLACK, (80, 50), (40, 50), 4)
        pygame.draw.line(screen, const.BLACK, (40, 50), (60, 60), 4)
        pygame.draw.line(screen, const.BLACK, (40, 50), (60, 40), 4)

        self.back_button.draw(screen)

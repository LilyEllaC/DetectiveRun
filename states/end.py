import pygame

from states.base import GameState

import ui
import utility
import resources
import vector2
import const


class EndState(GameState):
    def __init__(self, manager):
        super().__init__(manager)

        self.final_score = 0

        self.bg = resources.Resource(
            "assets/end.png",
            vector2.Vector2(2304, 1296),
            1,
            1,
            1,
            0.7,
            vector2.Vector2(0, 0),
        )

        self.restart_button = ui.Button(
            const.WIDTH // 2 - 100,
            const.HEIGHT - 120,
            200,
            100,
            "RESTART",
            const.FONT40,
            const.GREEN,
            const.DARK_YELLOW,
            True,
        )

    def on_enter(self, **kwargs):
        print("--- Entering End ---")

        for key, value in kwargs.items():
            setattr(self, key, value)

    async def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.restart_button.is_hovered():
                    await self.manager.change_state("INTRO")

    def draw(self, screen):
        self.bg.draw_image(screen, vector2.Vector2(0, 0))

        utility.toScreen(
            screen, "You got hit :(", const.MC_FONT, const.WHITE, const.WIDTH // 2, 100
        )

        utility.toScreen(
            screen,
            "You had a score of: " + str(self.final_score),
            const.MC_FONT,
            const.YELLOW,
            const.WIDTH // 2,
            150,
        )

        fs = self.final_score

        if fs < 10:
            text = "How is a score that low even possible?"
        elif fs < 20:
            text = "Were you even playing?"
        elif fs < 50:
            text = "You're doing good"
        elif fs < 100:
            text = "You ran for a while"
        elif fs < 200:
            text = "You must be exhausted"
        elif fs < 300:
            text = "Wow, you must have practiced a long time"
        elif fs < 500:
            text = "That was great!"
        elif fs < 1000:
            text = "Wow, I didn't even know a score that high was possible"
        elif fs < 50000:
            text = "Cheater."
        else:
            text = "Cheater."

        utility.toScreen(
            screen,
            text,
            const.MC_FONT,
            const.GREEN,
            const.WIDTH // 2,
            const.HEIGHT // 2,
        )

        self.restart_button.draw(screen)

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
            const.WIDTH // 2 - 224, const.HEIGHT - 120, 224 * 2, 21 * 2, "", const.FONT40, (0, 0, 0, 0), (0, 0, 0, 0), False
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
        if fs > 50000:
            text = "Cheater."
        elif fs >= 1000:
            text = "WOW. You won. You managed to catch the murderer with your bare hands -er- wings"
        elif fs > 500:
            text = "Congratulations! Even thought the murderer escaped you, you gave enough information that the murder was caught"
        elif fs > 500:
            text = "Congratulations! Even thought the murderer escaped you, you gave enough information that the murder was caught"
        elif fs > 300:
            text = "That was a long chase, but sadly he managed to thwart both you and your fellow cops"
        elif fs > 200:
            text = "You're getting closer, but he just managed to escape both you and your colleagues"
        elif fs > 100:
            text = "You managed to see the escape vehicle, but he got away before your commerades could catch him"
        elif fs > 50:
            text = "You are getting closer, but he still got away"
        elif fs > 20:
            text = "The murderer just walked out of the door in front of you"          
        elif fs > 10:
            text = "The murderer escaped you before you even knew who he was"
        else:
            text = "The murder caught you"

        utility.toScreen(
            screen,
            text,
            const.MC_FONT,
            const.GREEN,
            const.WIDTH // 2,
            const.HEIGHT // 2,
        )

        endBtnImg = pygame.image.load("assets/EndBtn.png")
        endBtnImg = pygame.transform.scale(endBtnImg, (endBtnImg.get_width() * 2, endBtnImg.get_height() * 2))
        screen.blit(endBtnImg, (const.WIDTH // 2 - endBtnImg.get_width() // 2, const.HEIGHT - 120))

        self.restart_button.draw(screen)

import pygame

from states.base import GameState

import ui
import utility as utils
import resources
import vector2
import const

newHighScore=False

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

        self.overlay = pygame.Surface(
            (const.WIDTH - 180, const.HEIGHT - 180), pygame.SRCALPHA
        )

        self.newHighScore=False


        # self.restart_button = ui.Button(
        #     const.WIDTH // 2 - 224,
        #     const.HEIGHT - 120,
        #     224 * 2,
        #     21 * 2,
        #     "",
        #     const.FONT40,
        #     (0, 0, 0, 0),
        #     (0, 0, 0, 0),
        #     False,
        # )

        self.font = "minecraft"

        self.back_label = ui.Label("< Back to Main Menu")
        self.back_label.font_name = self.font
        self.back_label.font_size = 24
        self.back_label.colour = const.LIGHT_RED
        self.back_label.underline_on_hover = True

    def on_enter(self, **kwargs):
        print("--- Entering End ---")

        for key, value in kwargs.items():
            setattr(self, key, value)

    async def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.back_label.is_hovered():
                    await self.manager.change_state("INTRO")

    def draw(self, screen):
        self.bg.draw_image(screen, vector2.Vector2(0, 0))

        pygame.draw.rect(
            self.overlay, (0, 0, 0, 150), self.overlay.get_rect(), border_radius=25
        )

        overlay_x = (const.WIDTH - self.overlay.get_width()) // 2
        overlay_y = (const.HEIGHT - self.overlay.get_height()) // 2
        screen.blit(self.overlay, (overlay_x, overlay_y))

        text_base_y = 300

        text_base_y += utils.to_screen(
            screen,
            "Game over!",
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
            f"Your score was: {self.final_score}",
            self.font,
            20,
            const.WHITE,
            const.WIDTH / 2,
            text_base_y,
        )["height"]

        fs = self.final_score
        if fs > 50000:
            text = "Cheater."
        elif fs >= 1000:
            text = "WOW. You won. You managed to catch the murderer\nwith your bare hands -er- wings"
        elif fs > 350:
            text = "Congratulations! Even thought the murderer escaped you,\nyou gave enough information that the murder was caught"
        elif fs > 250:
            text = "That was a long chase, but sadly he managed\nto thwart both you and your fellow cops"
        elif fs > 175:
            text = "You're getting closer, but he just managed\nto escape both you and your colleagues"
        elif fs > 100:
            text = "You managed to see the escape vehicle, but he\ngotaway before your commerades could catch him"
        elif fs > 50:
            text = "You are getting closer, but he still got away"
        elif fs > 20:
            text = "The murderer just walked out of the door in front of you"
        elif fs > 10:
            text = "You can't find the murderer even with\nhim being one of 2 people in the room"
        elif fs > 0:
            text = "The murderer escaped you before you even knew who he was"
        else:
            text = "The murderer caught you"

        split_text = text.split("\n")

        text_base_y += 24

        text_base_y += utils.to_screen(
            screen,
            split_text,
            self.font,
            20,
            const.GREEN,
            const.WIDTH // 2,
            text_base_y,
        )["height"]

        text_base_y += 24

        if fs > int(utils.getFromFile("highScore.txt")):
	        utils.pushToFile(fs, "highScore.txt")
	        self.newHighScore = True

        if self.newHighScore:
	        text_base_y += utils.to_screen(
		        screen,
		        "New High Score!",
		        self.font,
		        24,
		        const.GREEN,
		        const.WIDTH // 2,
		        text_base_y,
	        )["height"]

	        text_base_y += 8

	        text_base_y += utils.to_screen(
		        screen,
		        f"High Score: {utils.getFromFile("highScore.txt")}",
		        self.font,
		        24,
		        const.GREEN,
                const.WIDTH // 2,
                text_base_y,
                )["height"]

        self.back_label.x = const.WIDTH // 2
        self.back_label.y = text_base_y

        self.back_label.draw(screen)

        # endBtnImg = pygame.image.load("assets/EndBtn.png")
        # endBtnImg = pygame.transform.scale(
        #     endBtnImg, (endBtnImg.get_width() * 2, endBtnImg.get_height() * 2)
        # )
        # screen.blit(
        #     endBtnImg,
        #     (const.WIDTH // 2 - endBtnImg.get_width() // 2, const.HEIGHT - 120),
        # )

        # self.restart_button.draw(screen)
        #showing high score

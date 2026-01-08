import pygame
import const
import resources
import utility
import ui
import vector2

from states.base import GameState


class IntroState(GameState):
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

        self.crow = resources.Resource(
            "assets/crow-Sheet.png",
            vector2.Vector2(64, 64),
            8,
            14,
            0,
            4,
            vector2.Vector2(0, 0),
        )

        self.crow.animation_cooldown = 100

        self.start_button = ui.Button(
            800,
            const.HEIGHT / 2 - 80,
            320,
            60,
            "Start",
            const.FONT20,
            const.WHITE,
            const.GRAY,
            True,
        )

        self.help_button = ui.Button(
            800,
            const.HEIGHT / 2,
            320,
            60,
            "How to play?",
            const.FONT20,
            const.WHITE,
            const.GRAY,
            True,
        )

        self.exit_button = ui.Button(
            800,
            const.HEIGHT / 2 + 80,
            320,
            60,
            "Exit",
            const.FONT20,
            const.WHITE,
            const.GRAY,
            True,
        )

        self.exit_button.textColour = const.LIGHT_RED

    def on_enter(self, **kwargs):
        print("--- Entering Intro ---")

        for key, value in kwargs.items():
            setattr(self, key, value)

    async def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.start_button.is_hovered():
                    await utility.fade_to_black(self.manager.screen)

                    await self.manager.change_state("PLAYING")

                elif self.help_button.is_hovered():
                    await utility.fade_to_black(self.manager.screen)

                    await self.manager.change_state("HELP")

                    # await utility.fade_from_black(self.manager.screen)

                elif self.exit_button.is_hovered():
                    await utility.fade_to_black(self.manager.screen)

                    self.manager.quit()

    def update(self, dt):
        current_time = pygame.time.get_ticks()

        if current_time - self.crow.last_update >= self.crow.animation_cooldown:
            self.crow.last_update = current_time

            if self.crow.frame >= 25:
                self.crow.frame = 0
            if self.crow.frame == 9:
                self.crow.frame = 17
            else:
                self.crow.frame += 1

    def draw(self, screen):
        self.bg.draw_image(screen, vector2.Vector2(0, 0))

        # utility.toScreen(
        #     screen, "Detective Run", const.FONT60, const.BLACK, const.WIDTH / 2, 100
        # )

        s = pygame.Surface(
            (const.WIDTH, const.HEIGHT), pygame.SRCALPHA
        )  # per-pixel alpha
        s.fill((0, 0, 0, 128))
        screen.blit(s, (0, 0))

        sdw = pygame.Surface((500, const.HEIGHT), pygame.SRCALPHA)  # per-pixel alpha
        sdw.fill((0, 0, 0, 255 * 0.3))
        screen.blit(sdw, (700, 0))

        utility.to_screen(screen, "Detective Run", "fancy", 50, const.WHITE, 950, 150)

        self.crow.draw_image(screen, vector2.Vector2(100, const.HEIGHT / 2 - 42))

        self.start_button.draw(screen)
        self.help_button.draw(screen)
        self.exit_button.draw(screen)

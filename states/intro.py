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
            "assets/start.png",
            vector2.Vector2(2304, 1296),
            1,
            1,
            1,
            0.7,
            vector2.Vector2(0, 0),
        )

        self.crow = ui.Spritesheet("assets/crow-Sheet.png")
        self.crow.frame_width = 64
        self.crow.frame_height = 64
        self.crow.scale = 4

        self.crow.add_animation("intro", 0, 9, 100, loop=True)
        self.crow.add_animation("idle", 16, 25, 100, loop=True)

        self.main_frame = ui.Frame()
        self.main_frame.x = 700
        self.main_frame.y = const.HEIGHT // 2 - 150
        self.main_frame.width = 400
        self.main_frame.height = 300
        self.main_frame.layout = "vertical"
        self.main_frame.gap = 10
        self.main_frame.cross_align = "center"
        # self.main_frame.background_colour = (0, 0, 0, 100)  # Optional debug bg

        # Start Button Frame
        self.start_frame = ui.Frame()
        self.start_frame.width = 350
        self.start_frame.height = 70
        self.start_frame.layout = "horizontal"
        self.start_frame.gap = 10
        self.start_frame.cross_align = "center"

        self.start_icon = ui.Icon("assets/icons/gamepad-2.svg")
        self.start_icon.width = 40
        self.start_icon.height = 40
        self.start_icon.colour = const.WHITE

        self.start_label = ui.Label()
        self.start_label.text = "Start"
        self.start_label.font_size = 28
        self.start_label.colour = const.WHITE
        self.start_label.underline_on_hover = True

        self.start_frame.add_child(self.start_icon)
        self.start_frame.add_child(self.start_label)
        self.main_frame.add_child(self.start_frame)

        # Help Button Frame
        self.help_frame = ui.Frame()
        self.help_frame.width = 350
        self.help_frame.height = 70
        self.help_frame.layout = "horizontal"
        self.help_frame.gap = 10
        self.help_frame.cross_align = "center"

        self.help_icon = ui.Icon("assets/icons/circle-question-mark.svg")
        self.help_icon.width = 40
        self.help_icon.height = 40
        self.help_icon.colour = const.WHITE

        self.help_label = ui.Label()
        self.help_label.text = "How to play?"
        self.help_label.font_size = 28
        self.help_label.colour = const.WHITE
        self.help_label.underline_on_hover = True

        self.help_frame.add_child(self.help_icon)
        self.help_frame.add_child(self.help_label)
        self.main_frame.add_child(self.help_frame)

        # Exit Button Frame
        self.exit_frame = ui.Frame()
        self.exit_frame.width = 350
        self.exit_frame.height = 70
        self.exit_frame.layout = "horizontal"
        self.exit_frame.gap = 10
        self.exit_frame.cross_align = "center"

        self.exit_icon = ui.Icon("assets/icons/log-out.svg")
        self.exit_icon.width = 40
        self.exit_icon.height = 40
        self.exit_icon.colour = const.LIGHT_RED

        self.exit_label = ui.Label()
        self.exit_label.text = "Exit"
        self.exit_label.font_size = 28
        self.exit_label.colour = const.LIGHT_RED
        self.exit_label.underline_on_hover = True

        self.exit_frame.add_child(self.exit_icon)
        self.exit_frame.add_child(self.exit_label)
        self.main_frame.add_child(self.exit_frame)

        self.first_start = True

    def on_enter(self, **kwargs):
        print("--- Entering Intro ---")

        for key, value in kwargs.items():
            setattr(self, key, value)

    async def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                # We need to check if the main frame is hovered first?
                # Actually, main_frame draws children. But children are drawn ON the main frame surface.
                # So children is_hovered won't work directly because their rects are local to the frame surface.
                # Only the main_frame.rect is accurate in screen coords.

                # To properly handle click on children, we need to transform mouse coords to frame local coords.
                mx, my = pygame.mouse.get_pos()

                # Check collision with frame-relative rects manually for now
                if self.main_frame.rect.collidepoint(mx, my):
                    # Mouse is inside main frame. Relative coords:
                    rel_x = mx - self.main_frame.x
                    rel_y = my - self.main_frame.y

                    if self.start_frame.rect.collidepoint(rel_x, rel_y):
                        self.first_start = False
                        await utility.fade_to_black(self.manager.screen)
                        await self.manager.change_state("PLAYING")

                    elif self.help_frame.rect.collidepoint(rel_x, rel_y):
                        await utility.fade_to_black(self.manager.screen)
                        await self.manager.change_state("HELP")

                    elif self.exit_frame.rect.collidepoint(rel_x, rel_y):
                        await utility.fade_to_black(self.manager.screen)
                        self.manager.quit()

    def update(self, dt):
        if self.first_start:
            self.crow.play("intro")
        else:
            self.crow.play("idle")

        self.crow.update()

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

        self.crow.draw(screen, 100, const.HEIGHT / 2 - 42)

        self.main_frame.draw(screen)

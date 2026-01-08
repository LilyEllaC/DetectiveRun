import pygame
import asyncio

from enum import Enum

import const
import utility

from states.intro import IntroState
from states.help import HelpState
from states.playing import PlayingState
from states.end import EndState

running = True


class GameStates(Enum):
    INTRO = 1
    PLAYING = 2
    END = 3
    HELP = 4


"""
# async def handle_events(state):
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             return None
#
#         if state == GameStates.INTRO:
#             if event.type == pygame.MOUSEBUTTONDOWN:
#                 if intro.startButton.is_hovered():
#                     await utility.fade_to_black()
#
#                     return GameStates.PLAYING
#                 elif intro.helpButton.is_hovered():
#                     await utility.fade_to_black()
#
#                     return GameStates.HELP
#                 elif intro.exitButton.is_hovered():
#                     await utility.fade_to_black()
#
#                     return None
#
#         if state == GameStates.HELP:
#             if event.type == pygame.MOUSEBUTTONDOWN:
#                 if help.backButton.is_hovered():
#                     await utility.fade_to_black()
#
#                     return GameStates.INTRO
#
#         if state == GameStates.PLAYING:
#             if event.type == pygame.KEYDOWN:
#                 # able to enter an answer
#                 if playing.question.existing:
#                     playing.question.getGuess(event)
#                 # moving the crow
#                 if (
#                     event.key == pygame.K_SPACE
#                     # if crow is on the ground
#                     and playing.crow.y == playing.crow.floor - playing.crow.height - 5
#                 ):
#                     playing.crow.yVelocity = -20 * const.FPS_SCALING
#                     playing.crow.jumpPressed = True
#
#                 if event.key == pygame.K_DOWN:
#                     playing.crow.faster = 1 * const.FPS_SCALING
#
#             if event.type == pygame.KEYUP:
#                 if event.key == pygame.K_DOWN:
#                     playing.crow.faster = 0
#
#             if event.type == pygame.MOUSEBUTTONDOWN:
#                 if (
#                     playing.question.box.is_hovered()
#                     and playing.question.checkIfNumber()
#                 ):
#                     playing.question.checkGuess()
#
#         if state == GameStates.END:
#             if event.type == pygame.MOUSEBUTTONDOWN:
#                 if end.restartButton.is_hovered():
#                     playing.reset()
#
#                     return GameStates.INTRO
#
#     return False
"""


class Game:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((const.WIDTH, const.HEIGHT), vsync=1)
        self.clock = pygame.time.Clock()
        self.running = True

        self.states = {
            "INTRO": IntroState(self),
            "HELP": HelpState(self),
            "PLAYING": PlayingState(self),
            "END": EndState(self),
        }

        self.current_state = None
        self.dirty = False

    async def change_state(self, target_state, **kwargs):
        if self.current_state:
            await self.current_state.on_leave()

        self.current_state = self.states[target_state]

        self.current_state.on_enter(**kwargs)
        self.dirty = True

    def quit(self):
        self.running = False

    async def run(self):
        await self.change_state("INTRO")

        fade_surface = pygame.Surface((const.WIDTH, const.HEIGHT))
        fade_surface.fill(const.BLACK)

        while self.running:
            events = pygame.event.get()

            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False

            if self.current_state:
                await self.current_state.handle_events(events)

                if not self.running:
                    break

                self.current_state.update(const.FPS_SCALING)

                self.current_state.draw(self.screen)

                if self.dirty:
                    await utility.fade_from_black(self.screen)
                    self.dirty = False

            pygame.display.flip()
            self.clock.tick(const.FPS)
            await asyncio.sleep(0)

        pygame.quit()


if __name__ == "__main__":
    new_game = Game()
    asyncio.run(new_game.run())

    pygame.quit()

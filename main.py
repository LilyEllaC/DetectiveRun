import time

import pygame
import asyncio

import const

import help
import intro
import playing
import end

from enum import Enum

import utility

pygame.init()

running = True


class GameStates(Enum):
    INTRO = 1
    PLAYING = 2
    END = 3
    HELP = 4


async def handle_events(state):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return None

        if state == GameStates.INTRO:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if intro.startButton.is_hovered():
                    return GameStates.PLAYING
                elif intro.helpButton.is_hovered():
                    await utility.fadeOutResource(intro.bg)
                    intro.bg.set_alpha(255)

                    help.showHelp()

                    await utility.fadeInResource(help.bg)

                    help.bg.set_alpha(255)

                    return GameStates.HELP
                elif intro.exitButton.is_hovered():
                    await utility.fadeOutResource(intro.bg)
                    intro.bg.set_alpha(0)

                    return None

        if state == GameStates.HELP:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if help.backButton.is_hovered():
                    return GameStates.INTRO

        if state == GameStates.PLAYING:
            if event.type == pygame.KEYDOWN:
                if (
                    event.key == pygame.K_SPACE
                    # if crow is on the ground
                    and playing.crow.y == playing.crow.floor - playing.crow.height - 5
                ):
                    playing.crow.yVelocity = -20 * const.FPS_SCALING
                    playing.crow.jumpPressed = True

                if event.key == pygame.K_DOWN:
                    playing.crow.faster = 1 * const.FPS_SCALING

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    playing.crow.faster = 0

        if state == GameStates.END:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if end.restartButton.is_hovered():
                    playing.reset()

                    return GameStates.INTRO

    return False


async def main():
    global running

    game_state = GameStates.INTRO

    while running:
        new_state = await handle_events(game_state)

        if new_state in GameStates:
            game_state = new_state
        elif new_state is None:
            running = False

        if game_state == GameStates.INTRO:
            intro.showIntro()
        elif game_state == GameStates.PLAYING:
            playing.playGame()

            if playing.crow.hasCollided(playing.obstacles):
                game_state = GameStates.END
        elif game_state == GameStates.END:
            end.endGame()
        elif game_state == GameStates.HELP:
            help.showHelp()

        pygame.display.flip()
        const.clock.tick(const.FPS)
        await asyncio.sleep(0)


if __name__ == "__main__":
    asyncio.run(main())
    pygame.quit()

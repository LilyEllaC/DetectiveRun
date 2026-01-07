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
game_state = None


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
                    await utility.fade_to_black()

                    return GameStates.PLAYING
                elif intro.helpButton.is_hovered():
                    await utility.fade_to_black()

                    return GameStates.HELP
                elif intro.exitButton.is_hovered():
                    await utility.fade_to_black()

                    return None

        if state == GameStates.HELP:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if help.backButton.is_hovered():
                    await utility.fade_to_black()

                    return GameStates.INTRO

        if state == GameStates.PLAYING:
            if event.type == pygame.KEYDOWN:
                # able to enter an answer
                if playing.question.existing:
                    playing.question.getGuess(event)
                # moving the crow
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

            if event.type == pygame.MOUSEBUTTONDOWN:
                if (
                    playing.question.box.is_hovered()
                    and playing.question.checkIfNumber()
                ):
                    playing.question.checkGuess()

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

        rendered = False

        if new_state in GameStates:
            game_state = new_state

            rendered = True

            # print("NEW STATE RENDER", game_state.name)
            globals()[game_state.name.lower()].render()

            await utility.fade_from_black()
        elif new_state is None:
            running = False
            break

        if game_state == GameStates.PLAYING:
            if playing.crow.hasCollided(playing.obstacles):
                game_state = GameStates.END

        if not rendered:
            # print("OLD STATE RENDER", game_state.name)

            globals()[game_state.name.lower()].render()

        pygame.display.flip()
        const.clock.tick(const.FPS)
        await asyncio.sleep(0)


if __name__ == "__main__":
    asyncio.run(main())
    pygame.quit()

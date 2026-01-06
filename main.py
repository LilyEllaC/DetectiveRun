import pygame 
import constants
import utility
import asyncio

# pylint: disable=no-member
pygame.init()

#running
running=True



async def main():
    global running

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


        #ending stuff
        pygame.display.flip()
        constants.clock.tick(constants.FPS)
        await asyncio.sleep(0)


if __name__ == "__main__":
    asyncio.run(main())
    pygame.quit()
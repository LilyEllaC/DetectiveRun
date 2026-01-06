import pygame 
import constants as c
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

        c.screen.fill(c.BLACK)
        #ending stuff
        pygame.display.flip()
        c.clock.tick(c.FPS)
        await asyncio.sleep(0)


if __name__ == "__main__":
    asyncio.run(main())
    pygame.quit()
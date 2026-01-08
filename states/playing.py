import pygame
import const
import resources
import vector2
import utility
import ui
import asyncio

from states.base import GameState


class PlayingState(GameState):
    def __init__(self, manager):
        super().__init__(manager)

        # 1. LOAD ASSETS (ONCE)
        self.tile_map = resources.Resource(
            "assets/Terrain.png",
            vector2.Vector2(32, 32),
            19,
            13,
            0,
            3,
            vector2.Vector2(0, 0),
        )

        self.crow_sheet = resources.Resource(
            "assets/crow-Sheet.png",
            vector2.Vector2(64, 64),
            8,
            14,
            0,
            4,
            vector2.Vector2(0, 0),
        )
        self.crow_sheet.animation_cooldown = 100

        self.bg = resources.Resource(
            "assets/game.png",
            vector2.Vector2(2304, 1296),
            1,
            1,
            0,
            0.65,
            vector2.Vector2(0, 0),
        )

    def on_enter(self, **kwargs):
        print("--- Entering Playing ---")
        self.reset_game()
        for key, value in kwargs.items():
            setattr(self, key, value)

    def reset_game(self):
        self.velocity = -5 * const.FPS_SCALING
        self.crow = ui.Player(150, 100, 100, 1 * const.FPS_SCALING**2, self.crow_sheet)

        self.groundOffset = 0
        self.groundOffsetBackground = 0

        self.obstacle_size = 50
        self.obstacle1 = ui.Obstacle(
            const.WIDTH + 20, self.obstacle_size, self.obstacle_size, self.velocity
        )
        self.obstacle2 = ui.Obstacle(
            const.WIDTH + const.WIDTH // 2,
            self.obstacle_size,
            self.obstacle_size,
            self.velocity,
        )
        self.obstacles = [self.obstacle1, self.obstacle2]

        self.sprites = pygame.sprite.Group()
        self.sprites.add(self.crow)
        self.sprites.add(self.obstacle1)
        self.sprites.add(self.obstacle2)

        ui.obstacleImages = ["assets/crate.png", "assets/Box.png", "assets/Bomb.png"]
        self.question = ui.Question(const.WIDTH // 2, const.HEIGHT // 2, 300, 200)

    async def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if self.question.existing:
                    self.question.getGuess(event)

                if event.key == pygame.K_SPACE and (
                    self.crow.y == self.crow.floor - self.crow.height - 5
                    or self.crow.flying
                ):
                    self.crow.yVelocity = -20 * const.FPS_SCALING
                    self.crow.jumpPressed = True

                if event.key == pygame.K_DOWN:
                    self.crow.faster = 20 * const.FPS_SCALING**2
                    if self.crow.yVelocity < 0:
                        self.crow.yVelocity = 10 * const.FPS_SCALING

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    self.crow.faster = 0

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.question.box.is_hovered() and self.question.checkIfNumber():
                    if not self.question.checkGuess():
                        self.velocity += 0.5
                    else:
                        self.crow.flying=True
                        self.velocity/=1.25

    # --- MATH & LOGIC ONLY ---
    def update(self, dt):
        # 1. Update Background Offsets
        bg_width = 2304 * 0.65
        if not self.question.existing:
            self.groundOffsetBackground += abs(self.velocity) * 0.5
            if self.groundOffsetBackground >= bg_width:
                self.groundOffsetBackground -= bg_width

            tile_width = 32 * 3
            self.groundOffset += abs(self.velocity)
            if self.groundOffset >= tile_width:
                self.groundOffset -= tile_width

        # Update background after a score of 250
        if 150 <= self.crow.points and self.bg.path != "assets/game2.png":
            self.bg.tile_map_image = pygame.image.load(
                "assets/game2.png"
            ).convert_alpha()
            self.bg.path = "assets/game2.png"

        # 2. Game Logic
        if not self.question.existing:
            self.crow.move(self.question)
            self.crow.jump()
            self.crow.stopFlying()

        # 3. Obstacle Logic
        for obstacle in self.obstacles:
            obstacle.move(self.velocity, self.question)
            # Pass only the Question object, not the class
            obstacle.hasPassedPlayer(self.crow, self.question)

            if obstacle.x < -obstacle.width:
                obstacle.reset()

        # 4. Question Logic
        self.obstacle1.askQuestion(self.question)
        self.velocity -= 0.002 * const.FPS_SCALING

        if self.question.existing:
            if self.question.time == 0 + 1 / const.FPS:
                self.question.correct = False
                self.velocity += 0.75

        # 5. Collision (Death) Logic
        # Note: You need a hasCollided method on your Player class!
        if self.crow.hasCollided(self.obstacles):
            asyncio.create_task(
                self.manager.change_state("END", final_score=round(self.crow.points))
            )

        # having a new obstacle type added
        if self.crow.points > 300:
            ui.obstacleImages = [
                "assets/crate.png",
                "assets/Box.png",
                "assets/Bomb.png",
                "assets/start.png",
            ]

    # --- DRAWING PIXELS ONLY ---
    def draw(self, screen):
        screen.fill(const.DARK_GRAY_BLUE)

        # 1. Draw Background
        bg_width = 2304 * 0.65
        for i in range(3):
            x_pos = int((i * bg_width) - self.groundOffsetBackground)
            self.bg.draw_image(screen, vector2.Vector2(x_pos, -70))

        # 2. Draw Tiles
        self.tile_map.frame = 21
        tile_width = 32 * 3
        tiles_needed = (const.WIDTH // tile_width) + 2

        for i in range(tiles_needed):
            x_pos = int((i * tile_width) - self.groundOffset)
            self.tile_map.draw_image(screen, vector2.Vector2(x_pos, const.HEIGHT - 70))

        # 3. Draw Sprites (Crow + Obstacles)
        # We manually draw to ensure layering or use sprite group
        self.sprites.draw(screen)

        # 4. Draw Score
        self.crow.displayPoints(screen)

        # 5. Draw Question UI
        if self.question.existing:
            self.question.draw(screen)

            if self.question.answerSubmitted:
                if self.question.correct:
                    utility.toScreen(
                        screen,
                        "You got it right!",
                        const.FONT30,
                        const.GREEN,
                        self.question.x,
                        self.question.y + 50,
                    )
                else:
                    utility.toScreen2(
                        screen,
                        "That wasn't the answer",
                        "The right answer is " + str(self.question.answer),
                        const.FONT30,
                        const.RED,
                        self.question.x,
                        self.question.y + 50,
                    )
            elif not self.question.correct:
                utility.toScreen2(
                    screen,
                    "You ran out of time.",
                    "The right answer is " + str(self.question.answer),
                    const.FONT30,
                    const.RED,
                    self.question.x,
                    self.question.y + 50,
                )

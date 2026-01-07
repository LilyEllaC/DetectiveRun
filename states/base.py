class GameState:
    def __init__(self, manager):
        self.manager = manager

    def on_enter(self, **kwargs):
        pass

    async def on_leave(self):
        pass

    async def handle_events(self, events):
        pass

    def update(self, dt):
        pass

    def draw(self, screen):
        pass

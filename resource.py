import pygame
import vector2


class Resource:
    def __init__(self, path, frameSize, hFrames, vFrames, frame, scale, position):
        # 1. Load the image directly within the class
        try:
            # .convert_alpha() is crucial for performance and transparency in Pygame
            self.tilemap_image = pygame.image.load(path).convert_alpha()
            self.is_loaded = True
        except Exception as e:
            print(f"Error loading image '{path}': {e}")
            self.tilemap_image = None
            self.is_loaded = False

        self.frameSize = frameSize
        self.hFrames = hFrames
        self.vFrames = vFrames
        self.frame = frame
        self.scale = scale
        self.position = position
        self.frameMap = dict()
        self.alpha = 255
        self.animation_cooldown = 0
        self.last_update = 0

        # 2. Build the frame map immediately
        self.buildFrameMap()

    def buildFrameMap(self):
        frameCount = 0
        for v in range(0, self.vFrames):
            for h in range(0, self.hFrames):
                self.frameMap[frameCount] = vector2.Vector2(
                    h * self.frameSize.x, v * self.frameSize.y
                )
                frameCount += 1

    def drawImage(self, screen, position):
        screen.blit(self.getImage(), (position.x, position.y))

    def getImage(self):
        if not self.is_loaded or self.tilemap_image is None:
            # print("Resource has not been loaded") # Optional: silent fail is often better in loops
            return

        # 3. Get coordinates for the current frame
        frame_pos = self.frameMap.get(self.frame)

        # Default to 0,0 if frame not found (safety check)
        if not frame_pos:
            frame_coord_x = 0
            frame_coord_y = 0
        else:
            frame_coord_x = frame_pos.x
            frame_coord_y = frame_pos.y

        frame_size_x = self.frameSize.x
        frame_size_y = self.frameSize.y

        # Define the area of the sprite sheet we want to cut out
        src_rect = pygame.Rect(frame_coord_x, frame_coord_y, frame_size_x, frame_size_y)

        # Create a subsurface (fast crop)
        image_to_draw = self.tilemap_image.subsurface(src_rect)

        # Handle Scaling
        if self.scale != 1.0:
            target_width = int(frame_size_x * self.scale)
            target_height = int(frame_size_y * self.scale)
            image_to_draw = pygame.transform.scale(
                image_to_draw, (target_width, target_height)
            )

        image_to_draw.set_alpha(self.alpha)

        return image_to_draw

    def setAlpha(self, alpha):
        self.alpha = alpha

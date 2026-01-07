import pygame
import vector2


class Resource:
    def __init__(self, path, frame_size, h_frames, v_frames, frame, scale, position):
        try:
            self.tile_map_image = pygame.image.load(path).convert_alpha()
            self.is_loaded = True
        except Exception as e:
            print(f"Error loading image '{path}': {e}")

            self.tile_map_image = None
            self.is_loaded = False

        self.frame_size = frame_size
        self.h_frames = h_frames
        self.v_frames = v_frames
        self.frame = frame
        self.scale = scale
        self.position = position
        self.frame_map = dict()
        self.alpha = 255
        self.animation_cooldown = 0
        self.last_update = 0

        # 2. Build the frame map immediately
        self.build_frame_map()

    def build_frame_map(self):
        frame_count = 0

        for v in range(0, self.v_frames):
            for h in range(0, self.h_frames):
                self.frame_map[frame_count] = vector2.Vector2(
                    h * self.frame_size.x, v * self.frame_size.y
                )

                frame_count += 1

    def draw_image(self, screen, position):
        screen.blit(self.get_image(), (position.x, position.y))

    def get_image(self):
        if not self.is_loaded or self.tile_map_image is None:
            return None

        frame_pos = self.frame_map.get(self.frame)

        if not frame_pos:
            frame_coord_x = 0
            frame_coord_y = 0
        else:
            frame_coord_x = frame_pos.x
            frame_coord_y = frame_pos.y

        frame_size_x = self.frame_size.x
        frame_size_y = self.frame_size.y

        src_rect = pygame.Rect(frame_coord_x, frame_coord_y, frame_size_x, frame_size_y)

        image_to_draw = self.tile_map_image.subsurface(src_rect)

        if self.scale != 1.0:
            target_width = int(frame_size_x * self.scale)
            target_height = int(frame_size_y * self.scale)
            image_to_draw = pygame.transform.scale(
                image_to_draw, (target_width, target_height)
            )

        image_to_draw.set_alpha(self.alpha)

        return image_to_draw

    def set_alpha(self, alpha):
        self.alpha = alpha

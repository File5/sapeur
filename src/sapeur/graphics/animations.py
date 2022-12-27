import arcade
from pathlib import Path
from typing import Union, Tuple


class SpritesheetAnimation(arcade.AnimatedTimeBasedSprite):
    def __init__(self, file_name: Union[str, Path], sprite_width: int, sprite_height: int, columns: int, count: int, total_time_ms: int):
        super().__init__()
        self.textures = arcade.load_spritesheet(file_name, sprite_width, sprite_height, columns, count)
        self.frames = [arcade.AnimationKeyframe(i, total_time_ms / count, t) for i, t in enumerate(self.textures)]
        self.running = False

    def update_animation(self, delta_time: float = 1 / 60):
        if self.running:
            prev_frame_idx = self.cur_frame_idx
            super().update_animation(delta_time)
            if self.cur_frame_idx < prev_frame_idx:
                # animation ended
                self.running = False
                self.texture = self.frames[-1].texture

    def reset(self):
        self.running = False
        self.cur_frame_idx = 0
        self.texture = self.frames[0].texture


class ExplosionAnimation(SpritesheetAnimation):
    def __init__(self, **kwargs):
        super().__init__(":resources:images/spritesheets/explosion.png", 256, 256, 16, 16 * 14, 1500)

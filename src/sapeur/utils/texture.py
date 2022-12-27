import arcade
from pathlib import Path
from typing import Union, Tuple


class TextureSheet:
    def __init__(self,
                 file_path: Union[str, Path],
                 sprite_width: int,
                 sprite_height: int,
                 columns: int,
                 count: int,
                 margin: int = 0):
        self.columns = columns
        self.spritesheet = arcade.load_spritesheet(file_path, sprite_width, sprite_height, columns, count, margin)

    def __getitem__(self, item: Union[int, Tuple[int, int]]):
        if isinstance(item, int):
            return self.spritesheet[item]
        elif isinstance(item, tuple):
            return self.spritesheet[(item[0] - 1) * self.columns + (item[1] - 1)]


class TextureSheetSprite(arcade.Sprite):
    def __init__(self, texture_sheet: TextureSheet, index: Union[int, Tuple[int, int]], **kwargs):
        kwargs.pop("texture", None)
        super().__init__(texture=texture_sheet[index], **kwargs)
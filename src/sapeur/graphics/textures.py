import arcade
from typing import Union, Tuple
from sapeur.utils.texture import TextureSheet, TextureSheetSprite


class GeneralIconsTextureSheet(TextureSheet):
    def __init__(self):
        super().__init__("assets/general_icons.png", 32, 32, 16, 16 * 20)


class GeneralIconsSprite(TextureSheetSprite):
    def __init__(self, general_icons: GeneralIconsTextureSheet, index: Union[int, Tuple[int, int]], **kwargs):
        if type(general_icons) is not GeneralIconsTextureSheet:
            raise TypeError("general_icons must be an instance of GeneralIconsTextureSheet")
        super().__init__(general_icons, index, **kwargs)


class BombSprite(GeneralIconsSprite):
    def __init__(self, general_icons: GeneralIconsTextureSheet, **kwargs):
        super().__init__(general_icons, (11, 13), **kwargs)


class WoodSprite(GeneralIconsSprite):
    def __init__(self, general_icons: GeneralIconsTextureSheet, **kwargs):
        super().__init__(general_icons, (18, 1), **kwargs)


class TreeSprite(arcade.Sprite):
    def __init__(self, **kwargs):
        super().__init__("assets/tree.png", **kwargs)


class FlagSprite(arcade.Sprite):
    def __init__(self, **kwargs):
        super().__init__(":resources:images/items/flagRed2.png", **kwargs)


class FlagBSprite(arcade.Sprite):
    def __init__(self, color, **kwargs):
        assert color in ("red", "yellow", "green"), "unsupported color"
        super().__init__(f"assets/flags/{color}_flag.png", **kwargs)


class FlagSSprite(arcade.Sprite):
    def __init__(self, color, **kwargs):
        assert color in ("red", "yellow", "green"), "unsupported color"
        super().__init__(f"assets/flags_s/flags_s_{color}.png", **kwargs)


def FaceTexture(face):
    assert face in ("smile", "ohh", "win", "dead"), "unsupported face"
    return arcade.load_texture(f"assets/faces/{face}.png")


class FaceSprite(arcade.Sprite):
    def __init__(self, face, **kwargs):
        assert face in ("smile", "ohh", "win", "dead"), "unsupported face"
        super().__init__(f"assets/faces/{face}", **kwargs)
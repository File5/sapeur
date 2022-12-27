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

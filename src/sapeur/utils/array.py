from itertools import chain
from typing import Tuple, Union


class GridList(list):
    def __init__(self, width, height, default=None):
        super().__init__()
        self.width = width
        self.height = height
        self.default = default
        # col = [None for x in range(COLUMN_COUNT)]
        # row = [col for y in range(ROW_COUNT)]
        for y in range(height):
            self.append([default for x in range(width)])

    def __iter__(self):
        return chain(*tuple(super().__iter__()))

    def __len__(self) -> int:
        return self.width * self.height

    def __getitem__(self, item: Union[int, Tuple[int, int]]):
        if isinstance(item, tuple):
            return super().__getitem__(item[0])[item[1]]
        else:
            return super().__getitem__(item)

    def __setitem__(self, item: Union[int, Tuple[int, int]], value):
        if isinstance(item, tuple):
            return super().__getitem__(item[0]).__setitem__(item[1], value)
        else:
            return super().__setitem__(item, value)

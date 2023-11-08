from typing import Sequence, Union

import numpy as np
from multimethod import multimethod
from PIL.ImageColor import getrgb

__all__ = 'Color', 'ColorLike'


class Color:
    r: int
    g: int
    b: int
    a: int

    @multimethod
    def __init__(self, r: Union[int, np.uint8], g: Union[int, np.uint8], b: Union[int, np.uint8],
                 a: Union[int, np.uint8] = 255):
        super().__init__()
        self.r, self.g, self.b, self.a = int(r), int(g), int(b), int(a)

    @__init__.register
    def __init__(self, rgba: Sequence[Union[int, np.uint8]]):
        self.__init__(*rgba)

    @__init__.register
    def __init__(self, rgb_or_name: str):
        self.__init__(*getrgb(rgb_or_name))

    @__init__.register
    def __init__(self, rgba: int):
        self.__init__(hex(rgba).replace('0x', '#'))

    @__init__.register
    def __init__(self, color: 'Color'):
        self.__init__(color.rgba)

    @property
    def rgb(self):
        return self.r, self.g, self.b

    @property
    def rgb_unit(self):
        return self.r / 255, self.g / 255, self.b / 255

    @property
    def rgba_unit(self):
        return self.r / 255, self.g / 255, self.b / 255, self.a / 255

    @property
    def rgba(self):
        return self.r, self.g, self.b, self.a

    @property
    def hex(self):
        components = self.rgba
        if components[-1] == 255:
            components = components[:-1]
        return '#' + ''.join(f'{x:02x}' for x in components)

    def __eq__(self, other: 'Color'):
        return (
            self.r == other.r and self.g == other.g and self.b == other.b and self.a == other.a
        )

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        return cls(v)

    def __repr__(self):
        return f'<Color {self.rgba}>'

    # presets
    Transparent: 'Color' = 0, 0, 0, 0
    Red: 'Color' = 255, 0, 0, 255
    Green: 'Color' = 0, 255, 0, 255
    Gray: 'Color' = 128, 128, 128, 255
    DarkGray: 'Color' = 64, 64, 64, 255
    ForestGreen: 'Color' = 34, 139, 34, 255
    Yellow: 'Color' = 255, 255, 0, 255
    Orange: 'Color' = 255, 165, 0, 255
    DarkOrange: 'Color' = 255, 140, 0, 255
    Blue: 'Color' = 0, 0, 255, 255
    Black: 'Color' = 0, 0, 0, 255
    White: 'Color' = 255, 255, 255, 255


for _attr, _kind in Color.__annotations__.items():
    if _kind == 'Color' and not isinstance(getattr(Color, _attr), Color):
        setattr(Color, _attr, Color(getattr(Color, _attr)))

ColorLike = Union[Color, str, int, Sequence[int]]

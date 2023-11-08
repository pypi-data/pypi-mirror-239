from abc import ABC, abstractmethod
from enum import Enum
from typing import Sequence, Tuple

import numpy as np
from pydantic import BaseModel, Extra

from .color import Color


class NoExtra(BaseModel):
    class Config:
        extra = Extra.forbid


class Primitive(ABC):
    """ Base class for all primitive drawing operations """

    @abstractmethod
    def shift(self, x: float, y: float):
        """ Return primitives with shifted coordinates"""


class StrokeLocation(Enum):
    """ Defines how the stroke is drawn """
    Inner, Central, Outer = range(-1, 2)


class Paste(Primitive, NoExtra):
    patch: np.ndarray
    top: int
    left: int

    class Config:
        arbitrary_types_allowed = True

    def shift(self, x, y):
        return self.copy(update={'top': y + self.top, 'left': x + self.left})


class Line(Primitive, NoExtra):
    start: Tuple[float, float]
    stop: Tuple[float, float]
    stroke_color: Color
    stroke_width: float
    dash: tuple = ()

    def shift(self, x, y):
        return self.copy(update={'start': (self.start[0] + x, self.start[1] + y),
                                 'stop': (self.stop[0] + x, self.stop[1] + y)})


class Circle(Primitive, NoExtra):
    center: Tuple[float, float]
    radius: float
    stroke_color: Color
    stroke_width: float
    dash: tuple = ()

    def shift(self, x, y):
        return self.copy(update={'center': (self.center[0] + x, self.center[1] + y)})


class Polygon(Primitive, NoExtra):
    points: Sequence[Tuple[float, float]]
    stroke_color: Color = Color.Transparent
    stroke_width: float = 0
    background_color: Color = Color.Transparent
    dash: tuple = ()

    def shift(self, x, y):
        return self.copy(update={'points': [(p[0] + x, p[1] + y) for p in self.points]})


class Rectangle(Primitive, NoExtra):
    top: float
    left: float
    width: float
    height: float
    stroke_color: Color = Color.Transparent
    stroke_width: float = 0
    stroke_location: StrokeLocation = StrokeLocation.Inner
    background_color: Color = Color.Transparent
    radius: float = 0
    dash: Tuple[float, ...] = ()

    def shift(self, x, y):
        return self.copy(update={'top': self.top + y, 'left': self.left + x})

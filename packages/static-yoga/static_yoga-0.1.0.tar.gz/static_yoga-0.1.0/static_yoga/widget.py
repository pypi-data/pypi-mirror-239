from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Iterable, Sequence

from .yoga import Flex, Layout, Percent
from .primitives import Primitive


class Widget(ABC):
    """
    Basic block for all UI elements. Knows how to position and draw itself given a layout
    """

    @abstractmethod
    def build(self) -> Flex:
        """ Return a layout box """

    @abstractmethod
    def draw(self, layout: Layout) -> Iterable[Drawable]:
        """ Yield primitive draw calls which will be used to render the widget """


Drawable = Primitive | tuple[Layout, Widget]


class PrimitiveWidget(Widget):
    def __init__(self, primitive: Primitive):
        self.primitive = primitive

    def build(self) -> Flex:
        return Flex(width=Percent(100), height=Percent(100))

    def draw(self, layout: Layout) -> Iterable[Drawable]:
        yield self.primitive

    @staticmethod
    def wrap(*instances) -> Sequence[Widget]:
        return tuple(PrimitiveWidget(x) if isinstance(x, Primitive) else x for x in instances)


class WidgetFactory(Widget):
    def __init__(self, widget: Widget):
        super().__init__()
        self._widget = widget

    def build(self) -> Flex:
        return self._widget.build()

    def draw(self, layout: Layout) -> Iterable[Drawable]:
        return self._widget.draw(layout)

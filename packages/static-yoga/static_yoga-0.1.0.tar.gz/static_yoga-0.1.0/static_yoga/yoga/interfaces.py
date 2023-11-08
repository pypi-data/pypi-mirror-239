from enum import Enum
from typing import NamedTuple, Union, Sequence, Type, Tuple, Any


class Auto:
    def __init__(self):
        raise RuntimeError


number = Union[int, float]


class Percent(NamedTuple):
    value: number


Amount = Union[Type[Auto], Percent, number]
MaybePercent = Union[number, Percent]

MarginLike = Union[Amount, Sequence[Amount]]
BorderLike = Union[number, Sequence[number]]
PaddingLike = Union[MaybePercent, Sequence[MaybePercent]]


class Direction(Enum):
    Row, Column, RowReverse, ColumnReverse = range(4)


class PositionType(Enum):
    Relative, Absolute = range(2)


class Wrap(Enum):
    NoWrap, Wrap, Reverse = range(3)

    @classmethod
    def from_bool(cls, x):
        if isinstance(x, bool):
            return cls.Wrap if x else cls.NoWrap
        return x


class Align(Enum):
    Auto, Start, Center, End, Stretch, Baseline, SpaceBetween, SpaceAround = range(8)

    @classmethod
    def from_auto(cls, x):
        if x is Auto:
            return cls.Auto
        return x


class Justify(Enum):
    Start, Center, End, SpaceBetween, SpaceAround, SpaceEvenly = range(6)


class Flex:
    def __init__(self, min_width: MaybePercent = None, width: Amount = Auto, max_width: MaybePercent = None,
                 min_height: MaybePercent = None, height: Amount = Auto, max_height: MaybePercent = None,
                 margin: MarginLike = 0, border: BorderLike = 0, padding: PaddingLike = 0,
                 grow: number = 0, shrink: number = 0, basis: Amount = Auto,
                 direction: Direction = Direction.Row, wrap: Union[Wrap, bool] = False,
                 align_content: Align = Align.Start, align_items: Align = Align.Stretch, align_self: Align = Align.Auto,
                 justify_content: Justify = Justify.Start, position_type: PositionType = PositionType.Relative,
                 aspect_ratio: float = None, children: Sequence['Flex'] = (), context: Any = None):
        # TODO: better values validation
        self.position_type = position_type
        self.justify_content = justify_content
        self.aspect_ratio = aspect_ratio
        self.align_self = Align.from_auto(align_self)
        self.align_items = Align.from_auto(align_items)
        self.align_content = Align.from_auto(align_content)
        self.wrap = Wrap.from_bool(wrap)
        self.padding = _broadcast(padding)
        self.border = _broadcast(border)
        self.margin = _broadcast(margin)
        self.max_height = max_height
        self.max_width = max_width
        self.min_height = min_height
        self.min_width = min_width
        self.direction = direction
        self.basis = basis
        self.width, self.height = width, height
        self.grow, self.shrink = grow, shrink
        self.children = tuple(children)
        self.context = context

    def align(self, width: number, height: number) -> 'Layout':
        from .bridge import align
        return align(self, width, height)


class BoxSides(NamedTuple):
    begin: float
    end: float
    top: float
    bottom: float

    @property
    def horizontal(self):
        return self.begin + self.end

    @property
    def vertical(self):
        return self.top + self.bottom


class Layout(NamedTuple):
    x: float
    y: float
    rx: float
    ry: float
    width: float
    height: float
    margin: BoxSides
    border: BoxSides
    padding: BoxSides
    flex: Flex
    children: Tuple['Layout', ...]

    @property
    def position(self):
        return self.x, self.y

    @property
    def size(self):
        return self.width, self.height

    @property
    def context(self):
        return self.flex.context


def _broadcast(x):
    if isinstance(x, (int, float, Percent)) or x is Auto:
        return (x,) * 4
    return x

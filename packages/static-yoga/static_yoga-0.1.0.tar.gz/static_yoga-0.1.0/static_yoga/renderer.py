from functools import partial
from typing import Sequence, Union

import drawSvg
import numpy as np
from drawSvg import DrawingBasicElement as Drawable
from multimethod import multimethod

from .utils import unwrap_primitives
from .primitives import Line, Polygon, Rectangle, Paste, Circle
from .widget import Widget

try:
    from pyvips import Image

    error_message = None
except OSError as e:
    if 'libvips.so' in str(e):
        error_message = 'The package `libvips` is not installed in your OS'
    elif 'libgobject-2.0.so.0' in str(e):
        error_message = (
            'Your pyvips installation is broken. To fix it type: '
            'pip uninstall -y pyvips && conda install --channel conda-forge pyvips'
        )
    else:
        raise


    class NoStatic(type):
        def __getattr__(self, item):
            if item in ['__origin__', '__args__']:
                raise AttributeError(item)
            raise OSError(error_message)


    class Image(metaclass=NoStatic):
        def __init__(self):
            raise OSError(error_message)


class Vips:
    def __init__(self):
        if error_message:
            raise OSError(error_message)

    @multimethod
    def to_svg(self, image, primitive) -> Drawable:
        raise TypeError(f"Cannot to_svg argument of type {type(primitive)}")

    @to_svg.register
    def to_svg(self, image, primitive: Line) -> Drawable:
        return drawSvg.Line(
            # TODO: add shifts?
            primitive.start[0], image.height - primitive.start[1],
            primitive.stop[0], image.height - primitive.stop[1],
            stroke=primitive.stroke_color.hex, stroke_width=primitive.stroke_width,
            stroke_dasharray=' '.join(map(str, primitive.dash)),
            fill='none', fill_opacity=0.0,
        )

    @to_svg.register
    def to_svg(self, image, primitive: Circle) -> Drawable:
        return drawSvg.Circle(
            cx=primitive.center[0], cy=image.height - primitive.center[1], r=primitive.radius,
            stroke=primitive.stroke_color.hex, stroke_width=primitive.stroke_width,
            stroke_dasharray=' '.join(map(str, primitive.dash)),
            fill='none', fill_opacity=0.0,
        )

    @to_svg.register
    def to_svg(self, image, primitive: Rectangle) -> Drawable:
        delta = primitive.stroke_width * primitive.stroke_location.value
        half_delta = delta * 0.5
        draw_rectangle = partial(
            drawSvg.Rectangle,
            x=primitive.left - half_delta, y=image.height - primitive.height - primitive.top - half_delta,
            width=primitive.width + delta, height=primitive.height + delta,
            stroke=primitive.stroke_color.hex, stroke_width=primitive.stroke_width,
            stroke_dasharray=' '.join(map(str, primitive.dash)),
            fill=primitive.background_color.hex, fill_opacity=primitive.background_color.a / 255,
        )
        if primitive.radius:
            return draw_rectangle(rx=primitive.radius, ry=primitive.radius)
        return draw_rectangle()

    @to_svg.register
    def to_svg(self, image, primitive: Polygon) -> Drawable:
        points_flat = []
        for point in primitive.points:
            points_flat.extend([point[0] + 0.5, image.height - point[1] + 0.5])

        return drawSvg.Lines(
            *points_flat, close=True,
            stroke=primitive.stroke_color.hex, stroke_width=primitive.stroke_width,
            stroke_dasharray=' '.join(map(str, primitive.dash)),
            fill=primitive.background_color.hex, fill_opacity=primitive.background_color.a / 255,
        )

    @multimethod
    def render(self, image, primitive):
        raise TypeError(f"Cannot render argument of type {type(primitive)}")

    @render.register
    def render(self, image, primitive: Union[Line, Rectangle, Polygon, Circle]) -> Image:
        drawing = drawSvg.Drawing(image.width, image.height)
        drawing.append(self.to_svg(image, primitive))
        return paste(image, Image.svgload_buffer(drawing.asSvg().encode()), 0, 0)

    @render.register
    def render(self, image, primitive: Paste) -> Image:
        return paste(image, primitive.patch, primitive.top, primitive.left)

    def draw(self, image, widgets: Sequence[Widget]) -> np.ndarray:
        shape = image.shape[1], image.shape[0]
        image = self.wrap(image)
        layouts = [w.build().align(*shape) for w in widgets]
        for widget, layout in zip(widgets, layouts, strict=True):
            for primitive in unwrap_primitives(widget, layout, int(layout.x), int(layout.y)):
                image = self.render(image, primitive)

        return self.encode(image)

    @staticmethod
    def wrap(image: np.ndarray) -> Image:
        assert image.dtype == np.uint8
        assert image.ndim in [2, 3]
        if image.ndim == 2:
            image = np.repeat(image[..., None], 3, axis=-1)
        else:
            assert image.shape[-1] in [3, 4], image.shape

        height, width, bands = image.shape
        linear = image.reshape(width * height * bands)
        return Image.new_from_memory(linear.data, width, height, bands, 'uchar').copy(interpretation='srgb')

    @staticmethod
    def encode(image):
        result = np.ndarray(
            buffer=image.write_to_memory(), dtype=np.uint8, shape=[image.height, image.width, image.bands]
        )[..., :3]
        # assert result.shape == (image.height, image.width, 3)
        assert result.dtype == np.uint8
        return result


def paste(image: Image, patch: np.ndarray | Image, top, left) -> Image:
    with patch if isinstance(patch, Image) else Vips.wrap(patch) as patch:
        return image.composite(patch, 'over', x=left, y=top)

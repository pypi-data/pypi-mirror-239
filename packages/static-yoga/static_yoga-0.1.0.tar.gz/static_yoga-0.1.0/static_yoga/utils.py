from .primitives import Primitive


def unwrap_primitives(widget, layout, shift_x, shift_y):
    for item in widget.draw(layout):
        if isinstance(item, Primitive):
            yield item.shift(int(shift_x), int(shift_y))
        else:
            child_layout, child_widget = item
            yield from unwrap_primitives(
                child_widget, child_layout,
                shift_x + child_layout.rx, shift_y + child_layout.ry,
            )

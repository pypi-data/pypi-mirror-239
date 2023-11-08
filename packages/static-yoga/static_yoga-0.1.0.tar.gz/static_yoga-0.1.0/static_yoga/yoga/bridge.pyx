# cython: language_level=3

from .bridge cimport *
from .interfaces import Flex, Layout, Auto, Percent, Direction, Wrap, Align, Justify, BoxSides, PositionType

ctypedef void (*Amount1)(YGNode *)
ctypedef void (*Amount2)(YGNode *, float)
ctypedef void (*Edge1)(YGNode *, YGEdge)
ctypedef void (*Edge2)(YGNode *, YGEdge, float)
ctypedef void (*AlignFunc)(YGNode *, YGAlign)

cdef inline void _amount(YGNode * node, value, Amount1 on_auto, Amount2 on_percent, Amount2 on_absolute):
    if value is Auto:
        on_auto(node)
    elif isinstance(value, Percent):
        on_percent(node, value.value)
    elif isinstance(value, (int, float)):
        on_absolute(node, value)
    else:
        raise TypeError(value)

cdef inline void _amount_edge(YGNode * node, values, Edge1 on_auto, Edge2 on_percent, Edge2 on_absolute):
    for idx, value in enumerate(values):
        if value is Auto:
            on_auto(node, _edge(idx))
        elif isinstance(value, Percent):
            on_percent(node, _edge(idx), value.value)
        elif isinstance(value, (int, float)):
            on_absolute(node, _edge(idx), value)
        else:
            raise TypeError(value)

cdef inline void _maybe_percent(YGNode * node, value, Amount2 on_percent, Amount2 on_absolute):
    if value is None:
        return
    _amount(node, value, NULL, on_percent, on_absolute)

cdef inline _edge(int idx):
    if idx == 0:
        return YGEdgeStart
    if idx == 1:
        return YGEdgeEnd
    if idx == 2:
        return YGEdgeTop
    if idx == 3:
        return YGEdgeBottom
    raise ValueError(idx)

cdef _align(AlignFunc func, YGNode * node, value):
    if value is Align.Auto:
        func(node, YGAlignAuto)
    elif value is Align.Start:
        func(node, YGAlignFlexStart)
    elif value is Align.Center:
        func(node, YGAlignCenter)
    elif value is Align.End:
        func(node, YGAlignFlexEnd)
    elif value is Align.Stretch:
        func(node, YGAlignStretch)
    elif value is Align.Baseline:
        func(node, YGAlignBaseline)
    elif value is Align.SpaceBetween:
        func(node, YGAlignSpaceBetween)
    elif value is Align.SpaceAround:
        func(node, YGAlignSpaceAround)
    else:
        raise TypeError(value)

cdef YGNode * forward(node: Flex):
    yg_node = new YGNode()

    try:
        # width
        _amount(yg_node, node.width, YGNodeStyleSetWidthAuto, YGNodeStyleSetWidthPercent, YGNodeStyleSetWidth)
        _maybe_percent(yg_node, node.min_width, YGNodeStyleSetMinWidthPercent, YGNodeStyleSetMinWidth)
        _maybe_percent(yg_node, node.max_width, YGNodeStyleSetMaxWidthPercent, YGNodeStyleSetMaxWidth)
        # height
        _amount(yg_node, node.height, YGNodeStyleSetHeightAuto, YGNodeStyleSetHeightPercent, YGNodeStyleSetHeight)
        _maybe_percent(yg_node, node.min_height, YGNodeStyleSetMinHeightPercent, YGNodeStyleSetMinHeight)
        _maybe_percent(yg_node, node.max_height, YGNodeStyleSetMaxHeightPercent, YGNodeStyleSetMaxHeight)
        # margin stuff
        _amount_edge(yg_node, node.margin, YGNodeStyleSetMarginAuto, YGNodeStyleSetMarginPercent, YGNodeStyleSetMargin)
        _amount_edge(yg_node, node.border, NULL, NULL, YGNodeStyleSetBorder)
        _amount_edge(yg_node, node.padding, NULL, YGNodeStyleSetPaddingPercent, YGNodeStyleSetPadding)

        # flex
        if node.direction is Direction.Row:
            YGNodeStyleSetFlexDirection(yg_node, YGFlexDirectionRow)
        elif node.direction is Direction.RowReverse:
            YGNodeStyleSetFlexDirection(yg_node, YGFlexDirectionRowReverse)
        elif node.direction is Direction.Column:
            YGNodeStyleSetFlexDirection(yg_node, YGFlexDirectionColumn)
        elif node.direction is Direction.ColumnReverse:
            YGNodeStyleSetFlexDirection(yg_node, YGFlexDirectionColumnReverse)
        else:
            raise TypeError(node.direction)

        if node.justify_content is Justify.Start:
            YGNodeStyleSetJustifyContent(yg_node, YGJustifyFlexStart)
        elif node.justify_content is Justify.Center:
            YGNodeStyleSetJustifyContent(yg_node, YGJustifyCenter)
        elif node.justify_content is Justify.End:
            YGNodeStyleSetJustifyContent(yg_node, YGJustifyFlexEnd)
        elif node.justify_content is Justify.SpaceBetween:
            YGNodeStyleSetJustifyContent(yg_node, YGJustifySpaceBetween)
        elif node.justify_content is Justify.SpaceAround:
            YGNodeStyleSetJustifyContent(yg_node, YGJustifySpaceAround)
        elif node.justify_content is Justify.SpaceEvenly:
            YGNodeStyleSetJustifyContent(yg_node, YGJustifySpaceEvenly)
        else:
            raise TypeError(node.justify_content)

        # align
        _align(YGNodeStyleSetAlignContent, yg_node, node.align_content)
        _align(YGNodeStyleSetAlignItems, yg_node, node.align_items)
        _align(YGNodeStyleSetAlignSelf, yg_node, node.align_self)

        # position
        if node.position_type is PositionType.Absolute:
            YGNodeStyleSetPositionType(yg_node, YGPositionTypeAbsolute)

        # stretching
        YGNodeStyleSetFlexGrow(yg_node, node.grow)
        YGNodeStyleSetFlexShrink(yg_node, node.shrink)
        _amount(
            yg_node, node.basis, YGNodeStyleSetFlexBasisAuto, YGNodeStyleSetFlexBasisPercent, YGNodeStyleSetFlexBasis
        )

        if node.wrap is Wrap.NoWrap:
            YGNodeStyleSetFlexWrap(yg_node, YGWrapNoWrap)
        elif node.wrap is Wrap.Wrap:
            YGNodeStyleSetFlexWrap(yg_node, YGWrapWrap)
        elif node.wrap is Wrap.Reverse:
            YGNodeStyleSetFlexWrap(yg_node, YGWrapWrapReverse)
        else:
            raise TypeError(node.wrap)

        if node.aspect_ratio is not None:
            YGNodeStyleSetAspectRatio(yg_node, node.aspect_ratio)

        for idx, child in enumerate(node.children):
            YGNodeInsertChild(yg_node, forward(child), idx)

    except:
        YGNodeFree(yg_node)
        raise

    return yg_node

cdef backward(YGNode * internal, external, x, y):
    layout = internal.getLayout()
    local_x, local_y = layout.position[0], layout.position[1]
    global_x, global_y = local_x + x, local_y + y
    return Layout(
        global_x, global_y, local_x, local_y,
        layout.dimensions[0], layout.dimensions[1],
        BoxSides(*(layout.margin[i] for i in range(4))),
        BoxSides(*(layout.border[i] for i in range(4))),
        BoxSides(*(layout.padding[i] for i in range(4))),
        flex=external, children=tuple(
            backward(YGNodeGetChild(internal, idx), child, global_x, global_y)
            for idx, child in enumerate(external.children)
        ),
    )

cpdef align(root: Flex, width: float, height: float):
    try:
        yg_root = forward(root)
        YGNodeCalculateLayout(yg_root, width, height, YGDirectionLTR)
        return backward(yg_root, root, 0, 0)

    finally:
        # gc can't automatically clean these objects
        YGNodeFree(yg_root)

from libc.stdint cimport uint32_t

cdef extern from "<array>" namespace "std" nogil:
    cdef cppclass array2 "std::array<float, 2>":
        array2() except+
        float& operator[](size_t)

    cdef cppclass array4 "std::array<float, 4>":
        array4() except+
        float& operator[](size_t)

cdef extern from "yoga/YGNode.cpp":
    pass

cdef extern from "yoga/YGLayout.cpp":
    pass

cdef extern from "yoga/YGEnums.cpp":
    pass

cdef extern from "yoga/YGLayout.h":
    cdef cppclass YGLayout:
        YGLayout() except +
        array2 dimensions
        array4 position, margin, border, padding

cdef extern from "yoga/YGNode.h":
    cdef cppclass YGNode:
        YGNode() except +
        YGLayout& getLayout()


cdef extern from "yoga/YGEnums.h":
    cdef enum YGDirection:
        YGDirectionInherit,
        YGDirectionLTR,
        YGDirectionRTL

    cdef enum YGEdge:
        YGEdgeLeft,
        YGEdgeTop,
        YGEdgeRight,
        YGEdgeBottom,
        YGEdgeStart,
        YGEdgeEnd,
        YGEdgeHorizontal,
        YGEdgeVertical,
        YGEdgeAll

    cdef enum YGFlexDirection:
        YGFlexDirectionColumn,
        YGFlexDirectionColumnReverse,
        YGFlexDirectionRow,
        YGFlexDirectionRowReverse

    cdef enum YGAlign:
        YGAlignAuto,
        YGAlignFlexStart,
        YGAlignCenter,
        YGAlignFlexEnd,
        YGAlignStretch,
        YGAlignBaseline,
        YGAlignSpaceBetween,
        YGAlignSpaceAround

    cdef enum YGJustify:
        YGJustifyFlexStart,
        YGJustifyCenter,
        YGJustifyFlexEnd,
        YGJustifySpaceBetween,
        YGJustifySpaceAround,
        YGJustifySpaceEvenly

    cdef enum YGOverflow:
        YGOverflowVisible,
        YGOverflowHidden,
        YGOverflowScroll

    cdef enum YGWrap:
        YGWrapNoWrap,
        YGWrapWrap,
        YGWrapWrapReverse

    cdef enum YGPositionType:
        YGPositionTypeStatic,
        YGPositionTypeRelative,
        YGPositionTypeAbsolute

cdef extern from "yoga/Yoga.h":
    # dims
    void YGNodeStyleSetWidth(YGNode * node, float & points)
    void YGNodeStyleSetWidthPercent(YGNode * node, float & percent)
    void YGNodeStyleSetWidthAuto(YGNode * node)
    void YGNodeStyleSetHeight(YGNode * node, float & points)
    void YGNodeStyleSetHeightPercent(YGNode * node, float & percent)
    void YGNodeStyleSetHeightAuto(YGNode * node)

    void YGNodeStyleSetMinWidth(YGNode * node, float minWidth)
    void YGNodeStyleSetMinWidthPercent(YGNode * node, float minWidth)
    void YGNodeStyleSetMinHeight(YGNode * node, float minHeight)
    void YGNodeStyleSetMinHeightPercent(YGNode * node, float minHeight)
    void YGNodeStyleSetMaxWidth(YGNode * node, float maxWidth)
    void YGNodeStyleSetMaxWidthPercent(YGNode * node, float maxWidth)
    void YGNodeStyleSetMaxHeight(YGNode * node, float maxHeight)
    void YGNodeStyleSetMaxHeightPercent(YGNode * node, float maxHeight)

    void YGNodeStyleSetMargin(YGNode * node, YGEdge edge, float margin)
    void YGNodeStyleSetMarginPercent(YGNode * node, YGEdge edge, float margin)
    void YGNodeStyleSetMarginAuto(YGNode * node, YGEdge edge)
    void YGNodeStyleSetPadding(YGNode * node, YGEdge edge, float padding)
    void YGNodeStyleSetPaddingPercent(YGNode * node, YGEdge edge, float padding)
    void YGNodeStyleSetBorder(YGNode * node, YGEdge edge, float border)

    # flex
    void YGNodeStyleSetFlexDirection(YGNode * node, YGFlexDirection flexDirection)
    void YGNodeStyleSetJustifyContent(YGNode * node, YGJustify justifyContent)
    void YGNodeStyleSetAlignContent(YGNode * node, YGAlign alignContent)
    void YGNodeStyleSetAlignItems(YGNode * node, YGAlign alignItems)
    void YGNodeStyleSetAlignSelf(YGNode * node, YGAlign alignSelf)
    void YGNodeStyleSetPositionType(YGNode * node, YGPositionType positionType)
    void YGNodeStyleSetFlexWrap(YGNode * node, YGWrap flexWrap)
    # void YGNodeStyleSetOverflow(YGNode * node, YGOverflow overflow)
    # void YGNodeStyleSetDisplay(YGNode * node, YGDisplay display)
    # void YGNodeStyleSetFlex(YGNode * node, float flex)
    void YGNodeStyleSetFlexGrow(YGNode * node, float flexGrow)
    void YGNodeStyleSetFlexShrink(YGNode * node, float flexShrink)
    void YGNodeStyleSetFlexBasis(YGNode * node, float flexBasis)
    void YGNodeStyleSetFlexBasisPercent(YGNode * node, float flexBasis)
    void YGNodeStyleSetFlexBasisAuto(YGNode * node)
    void YGNodeStyleSetAspectRatio(YGNode * node, float aspectRatio)

    # structure
    void YGNodeInsertChild(YGNode * owner, YGNode * child, uint32_t index)
    void YGNodeFree(YGNode * node)
    YGNode * YGNodeGetChild(YGNode * node, uint32_t index)
    void YGNodeCalculateLayout(YGNode * node, float ownerWidth, float ownerHeight, YGDirection ownerDirection)

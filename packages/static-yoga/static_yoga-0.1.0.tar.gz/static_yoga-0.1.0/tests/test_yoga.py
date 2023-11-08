from static_yoga import Flex, Justify


def test_align():
    root = Flex(
        justify_content=Justify.SpaceBetween,
        children=[
            Flex(100, 100),
            Flex(100, 100),
        ]
    ).align(1000, 1000)
    a, b = root.children
    assert a.position == (0, 0)
    assert a.size == (100, 1000)
    assert b.position == (900, 0)
    assert b.size == (100, 1000)

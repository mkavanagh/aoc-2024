from day04.commands import _diagonalise
from lib.lineutils import transpose


def test_diagonalise_lines():
    lines = [
        "x...",
        ".m..",
        "..a.",
        "...s"
    ]

    expected = [
        "   x...",
        "  .m.. ",
        " ..a.  ",
        "...s   "
    ]

    assert _diagonalise(lines) == expected

    expected = [
        ".   ",
        "..  ",
        "... ",
        "xmas",
        " ...",
        "  ..",
        "   ."
    ]

    assert transpose(_diagonalise(lines)) == expected

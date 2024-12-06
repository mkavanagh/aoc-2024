from day04.commands import _diagonalise_lines, _transpose_lines

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

    assert _diagonalise_lines(lines) == expected

    expected = [
        ".   ",
        "..  ",
        "... ",
        "xmas",
        " ...",
        "  ..",
        "   ."
    ]

    assert _transpose_lines(_diagonalise_lines(lines)) == expected


def test_transpose_lines():
    lines = [
        ".x..",
        ".m..",
        ".a..",
        ".s.."
    ]

    expected = [
        "....",
        "....",
        "xmas",
        "...."
    ]

    assert _transpose_lines(lines) == expected

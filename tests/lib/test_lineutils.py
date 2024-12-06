from lib.lineutils import transpose, replace_index


def test_transpose():
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

    assert transpose(lines) == expected


def test_replace_index():
    assert replace_index('abcd', 1, 'x') == 'axcd'
    assert replace_index('abcdef', 3, 'hello') == 'abchelloef'

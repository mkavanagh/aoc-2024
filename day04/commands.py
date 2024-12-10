"""Advent of Code 2024, Day 4."""

from lib.common import line_input
from lib.lineutils import flip, transpose


@line_input()
def get_xmas_count(lines: list[str]) -> int:
    return _count_wordsearch(lines, 'XMAS')


@line_input()
def get_masx_count(lines: list[str]) -> int:
    return _count_xword(lines, 'MAS')


def _count_wordsearch(lines: list[str], word: str) -> int:
    count = _count_occurrences(lines, word)
    transformed = transpose(lines)
    count += _count_occurrences(transformed, word)
    transformed = transpose(_diagonalise(lines))
    count += _count_occurrences(transformed, word)
    transformed = transpose(_diagonalise(flip(lines)))
    count += _count_occurrences(transformed, word)
    return count


def _count_occurrences(lines: list[str], word: str) -> int:
    count = 0
    word_reversed = word[::-1]
    for line in lines:
        count += line.count(word)
        count += line.count(word_reversed)
    return count


def _diagonalise(lines: list[str]) -> list[str]:
    return [
        (' ' * (len(lines) - (i + 1))) + line + (' ' * i)
        for i, line in enumerate(lines)
    ]


def _count_xword(lines: list[str], word: str) -> int:
    count = 0
    word_reversed = word[::-1]
    margin = len(word) - 1
    for y in range(0, len(lines) - margin):
        for x in range(0, len(lines[y]) - margin):
            count += _check_xword(lines, x, y, word, word_reversed)
    return count


def _check_xword(
    lines: list[str], x: int, y: int, word: str, word_reversed: str
) -> bool:
    return (
        _check_diagonal(lines, x, y, word)
        or _check_diagonal(lines, x, y, word_reversed)
    ) and (
        _check_reverse_diagonal(lines, x + (len(word) - 1), y, word)
        or _check_reverse_diagonal(lines, x + (len(word) - 1), y, word_reversed)
    )


def _check_diagonal(
    lines: list[str], x: int, y: int, word: str
) -> bool:
    return all(lines[y + i][x + i] == word[i] for i in range(0, len(word)))


def _check_reverse_diagonal(
    lines: list[str], x: int, y: int, word: str
) -> bool:
    return all(lines[y + i][x - i] == word[i] for i in range(0, len(word)))

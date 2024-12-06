"""Advent of Code 2024, Day 4."""

from lib.common import read_strings


def get_xmas_count(filename: str) -> int:
    lines = read_strings(filename)
    return _count_wordsearch(lines, 'XMAS')


def get_masx_count(filename: str) -> int:
    lines = read_strings(filename)
    return _count_xword(lines, 'MAS')


def _count_wordsearch(lines: list[str], word: str) -> int:
    count = _count_occurrences(lines, word)
    transformed = _transpose_lines(lines)
    count += _count_occurrences(transformed, word)
    transformed = _transpose_lines(_diagonalise_lines(lines))
    count += _count_occurrences(transformed, word)
    transformed = _transpose_lines(_diagonalise_lines(_flip_lines(lines)))
    count += _count_occurrences(transformed, word)
    return count


def _count_occurrences(lines: list[str], word: str) -> int:
    count = 0
    word_reversed = word[::-1]
    for line in lines:
        count += line.count(word)
        count += line.count(word_reversed)
    return count


def _transpose_lines(lines: list[str]) -> list[str]:
    if not lines:
        return []

    transposed = ['' for _ in range(0, len(lines[0]))]
    for line in lines:
        for i in range(0, len(line)):
            transposed[-(i + 1)] += line[i]
    return transposed


def _flip_lines(lines: list[str]) -> list[str]:
    flipped = list(lines)
    flipped.reverse()
    return flipped


def _diagonalise_lines(lines: list[str]) -> list[str]:
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

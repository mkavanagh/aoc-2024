from collections import defaultdict
from typing import Any, Callable

from lib.common import line_input


@line_input()
def get_precedence_rules(lines: list[str]) -> dict[int, set[int]]:
    _, precedence_rules = _parse_precedence_rules(lines)
    return precedence_rules


@line_input()
def get_valid_page_updates(lines: list[str]) -> list[list[int]]:
    i, precedence_rules = _parse_precedence_rules(lines)
    return [
        update
        for update in _parse_page_updates(lines, i)
        if _is_valid_update(precedence_rules, update)
    ]


@line_input()
def get_day5_part1(lines: list[str]) -> int:
    """A snowball's chance in hell of giving this a descriptive name."""
    i, precedence_rules = _parse_precedence_rules(lines)
    return sum(
        _get_middle_page(update)
        for update in _parse_page_updates(lines, i)
        if _is_valid_update(precedence_rules, update)
    )


@line_input()
def get_day5_part2(lines: list[str]) -> int:
    i, precedence_rules = _parse_precedence_rules(lines)
    return sum(
        _get_middle_page(_apply_precedence_rules(precedence_rules, update))
        for update in _parse_page_updates(lines, i)
        if not _is_valid_update(precedence_rules, update)
    )


def _parse_precedence_rules(
    lines: list[str]
) -> tuple[int, dict[int, set[int]]]:
    i = 0
    precedence_rules = defaultdict(set)
    for i, line in enumerate(lines):
        if not line:
            continue
        if '|' in line:
            (l, r) = line.split('|')
            precedence_rules[int(l)].add(int(r))
        else:
            break
    return i, precedence_rules


def _parse_page_updates(lines: list[str], i: int) -> list[list[int]]:
    return [
        [int(n) for n in line.split(',')]
        for line in lines[i:] if line
    ]


def _is_valid_update(
    precedence_rules: dict[int, set[int]], update: list[int]
) -> bool:
    seen = set()
    for page in update:
        if not precedence_rules[page].isdisjoint(seen):
            return False
        seen.add(page)
    return True


def _get_middle_page(update: list[int]) -> int:
    return update[int(len(update) / 2)]


def _apply_precedence_rules(
    precedence_rules: dict[int, set[int]], update: list[int]
) -> list[int]:
    return sorted(update, key=_get_precedence_key_func(precedence_rules))


def _get_precedence_key_func(
    precedence_rules: dict[int, set[int]]
) -> Callable[[int], Any]:
    class PrecedenceKey:
        __slots__ = 'value', 'appears_before'

        def __init__(self, value):
            self.value = value
            self.appears_before = precedence_rules[value]

        def __lt__(self, other):
            return other.value in self.appears_before

    return PrecedenceKey

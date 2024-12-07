import re

from day06.model import CELL_TYPES, PatrolBoard
from lib.cellular_automata import TracingBoard
from lib.common import read_strings
from lib.lineutils import replace_index


def get_patrolled_cell_count(filename: str) -> int:
    lines = read_strings(filename)
    patrol_map = TracingBoard(lines, CELL_TYPES)

    patrol_map.run()

    return sum(
        row.count('X') for row in patrol_map.rows
    )


def get_patrolled_route(filename: str) -> str:
    lines = read_strings(filename)
    patrol_map = TracingBoard(lines, CELL_TYPES)

    patrol_map.run()

    return '\n'.join(patrol_map.rows)


def get_looper_count(filename: str) -> int:
    original_lines = read_strings(filename)
    rows = list(original_lines)
    original_map = PatrolBoard(rows, CELL_TYPES)

    original_map.run()

    cleaned_lines = [re.sub('\\^v<>', '.', line) for line in original_lines]

    looper_count = 0
    tried = set()
    for x, (i, j, _) in enumerate(original_map.route):
        if x > 0 and not (i, j) in tried:
            tried.add((i, j))

            new_lines = list(cleaned_lines)
            new_lines[i] = replace_index(new_lines[i], j, '#')

            new_map = TracingBoard(new_lines, CELL_TYPES)

            previous = original_map.route[x - 1]
            new_map.replace(
                previous[0], previous[1],
                previous[2], CELL_TYPES[previous[2]]
            )

            new_map.run()

            looper_count += new_map.looped
    return looper_count

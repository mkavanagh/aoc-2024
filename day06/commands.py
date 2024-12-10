import re

from day06.model import CELL_TYPES, PatrolBoard, TracingBoard
from lib.cellular_automata import Board
from lib.common import line_input
from lib.lineutils import replace_index

guard_matcher = re.compile('[\\^v<>]')


@line_input()
def get_patrolled_cell_count(lines: list[str]) -> int:
    patrol_map = Board(lines, CELL_TYPES)

    patrol_map.run()

    return sum(
        len(guard_matcher.findall(row)) for row in patrol_map.rows
    )


@line_input()
def get_patrolled_route(lines: list[str]) -> str:
    patrol_map = Board(lines, CELL_TYPES)

    patrol_map.run()

    return '\n'.join(patrol_map.rows)


@line_input()
def get_looper_count(original_lines: list[str]) -> int:
    rows = list(original_lines)
    original_map = PatrolBoard(rows, CELL_TYPES)

    guard_locations = set(original_map.live_cells.keys())

    original_map.run()

    for i, j in guard_locations:
        original_lines[i] = replace_index(original_lines[i], j, '.')

    looper_count = 0
    tried = set(guard_locations)
    for x, (i, j, _) in enumerate(original_map.route):
        if not (i, j) in tried:
            tried.add((i, j))

            new_lines = list(original_lines)
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

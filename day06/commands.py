from day06.model import load_board
from lib.common import read_strings
from lib.lineutils import replace_index


def get_patrolled_cell_count(filename: str) -> int:
    lines = read_strings(filename)
    patrol_map = load_board(lines)

    patrol_map.run()

    return sum(
        row.count('X') for row in patrol_map.rows
    )


def get_patrolled_route(filename: str) -> str:
    lines = read_strings(filename)
    patrol_map = load_board(lines)

    patrol_map.run()

    return '\n'.join(patrol_map.rows)


def get_looper_count(filename: str) -> int:
    original_lines = read_strings(filename)
    original_map = load_board(list(original_lines))

    original_map.run()

    looper_count = 0
    for i, j in set(original_map.route[1:]):
        new_lines = list(original_lines)
        new_lines[i] = replace_index(new_lines[i], j, '#')
        new_map = load_board(new_lines)
        new_map.run()
        looper_count += new_map.looped
    return looper_count

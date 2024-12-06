from day06.model import load_board
from lib.common import read_strings


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

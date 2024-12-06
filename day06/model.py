from collections import defaultdict
from typing import Optional

from lib.cellular_automata import Board, Cell


class GuardUpCell(Cell):
    def update(self):
        up = self._cell_up()
        if up == '#':
            self._replace_self('>', GuardRightCell)
        else:
            self._replace_up('^', GuardUpCell)
            self._replace_self('X')


class GuardDownCell(Cell):
    def update(self):
        down = self._cell_down()
        if down == '#':
            self._replace_self('<', GuardLeftCell)
        else:
            self._replace_down('v', GuardDownCell)
            self._replace_self('X')


class GuardLeftCell(Cell):
    def update(self):
        left = self._cell_left()
        if left == '#':
            self._replace_self('^', GuardUpCell)
        else:
            self._replace_left('<', GuardLeftCell)
            self._replace_self('X')


class GuardRightCell(Cell):
    def update(self):
        right = self._cell_right()
        if right == '#':
            self._replace_self('v', GuardDownCell)
        else:
            self._replace_right('>', GuardRightCell)
            self._replace_self('X')


CELL_TYPES: dict[str, type(Cell)] = {
    '^': GuardUpCell,
    'v': GuardDownCell,
    '<': GuardLeftCell,
    '>': GuardRightCell
}


class TracingBoard(Board):
    __slots__ = 'past_chars', 'looped'

    past_chars: dict[tuple[int, int], set[str]]
    looped: bool

    def __init__(self, rows: list[str], cell_types: dict[str, type(Cell)]):
        super().__init__(rows, cell_types)
        self.past_chars = defaultdict(set)
        self.looped = False

    def run(self) -> None:
        while self.step() and not self.looped:
            pass

    def replace(
        self, i: int, j: int, char: str, cell_type: Optional[type(Cell)] = None
    ) -> bool:
        if super().replace(i, j, char, cell_type):
            self.past_chars[(i, j)].add(self.rows[i][j])
            if char in self.past_chars:
                self.looped = True
            return True
        return False


def load_board(rows: list[str]) -> TracingBoard:
    return TracingBoard(rows, CELL_TYPES)

from typing import Optional

from lib.cellular_automata import Board, Cell


class GuardUpCell(Cell):
    def update(self):
        up = self._cell_up()
        if up == '#':
            self._replace_self('>', GuardRightCell)
        else:
            self._replace_up('^', GuardUpCell)


class GuardDownCell(Cell):
    def update(self):
        down = self._cell_down()
        if down == '#':
            self._replace_self('<', GuardLeftCell)
        else:
            self._replace_down('v', GuardDownCell)


class GuardLeftCell(Cell):
    def update(self):
        left = self._cell_left()
        if left == '#':
            self._replace_self('^', GuardUpCell)
        else:
            self._replace_left('<', GuardLeftCell)


class GuardRightCell(Cell):
    def update(self):
        right = self._cell_right()
        if right == '#':
            self._replace_self('v', GuardDownCell)
        else:
            self._replace_right('>', GuardRightCell)


CELL_TYPES: dict[str, type(Cell)] = {
    '^': GuardUpCell,
    'v': GuardDownCell,
    '<': GuardLeftCell,
    '>': GuardRightCell
}


class PatrolBoard(Board):
    __slots__ = 'route'

    route: list[tuple[int, int, str]]

    def __init__(self, rows: list[str], cell_types: dict[str, type(Cell)]):
        super().__init__(rows, cell_types)
        self.route = []

    def replace(
        self, i: int, j: int, char: str, cell_type: Optional[type(Cell)] = None
    ) -> Optional[str]:
        replaced = super().replace(i, j, char, cell_type)
        if replaced:
            self.route.append((i, j, char))
        return replaced


class TracingBoard(Board):
    __slots__ = 'looped'

    looped: bool

    def __init__(self, rows: list[str], cell_types: dict[str, type(Cell)]):
        super().__init__(rows, cell_types)
        self.looped = False

    def run(self) -> None:
        while self.step() and not self.looped:
            pass

    def replace(
        self, i: int, j: int, char: str, cell_type: Optional[type(Cell)] = None
    ) -> Optional[str]:
        if 0 <= i < len(self.rows) and 0 <= j < len(self.rows[i]):
            old_char = self.rows[i][j]
            if old_char in CELL_TYPES:
                if old_char == char:
                    self.looped = True
                char = old_char
        return super().replace(i, j, char, cell_type)

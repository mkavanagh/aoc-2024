from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional

from lib.lineutils import replace_index


class Cell(ABC):
    __slots__ = 'patrol_map', 'i', 'j'

    patrol_map: PatrolMap
    i: int
    j: int

    def __init__(self, patrol_map: PatrolMap, i: int, j: int):
        self.patrol_map = patrol_map
        self.i = i
        self.j = j

    @abstractmethod
    def update(self):
        pass

    def _cell_up(self) -> Optional[str]:
        if self.i >= 0:
            return self.patrol_map.rows[self.i - 1][self.j]
        return None

    def _cell_down(self) -> Optional[str]:
        if self.i + 1 < len(self.patrol_map.rows):
            return self.patrol_map.rows[self.i + 1][self.j]
        return None

    def _cell_left(self) -> Optional[str]:
        row = self.patrol_map.rows[self.i]
        if self.j > 0:
            return row[self.j - 1]
        return None

    def _cell_right(self) -> Optional[str]:
        row = self.patrol_map.rows[self.i]
        if self.j + 1 < len(row):
            return row[self.j + 1]
        return None

    def _replace_self(
        self, char: str, cell_type: Optional[type(Cell)] = None
    ) -> None:
        self.patrol_map.replace(self.i, self.j, char, cell_type)

    def _replace_up(
        self, char: str, cell_type: Optional[type(Cell)] = None
    ) -> None:
        self.patrol_map.replace(self.i - 1, self.j, char, cell_type)

    def _replace_down(
        self, char: str, cell_type: Optional[type(Cell)] = None
    ) -> None:
        self.patrol_map.replace(self.i + 1, self.j, char, cell_type)

    def _replace_left(
        self, char: str, cell_type: Optional[type(Cell)] = None
    ) -> None:
        self.patrol_map.replace(self.i, self.j - 1, char, cell_type)

    def _replace_right(
        self, char: str, cell_type: Optional[type(Cell)] = None
    ) -> None:
        self.patrol_map.replace(self.i, self.j + 1, char, cell_type)


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


GUARD_TYPES: dict[str, type(Cell)] = {
    '^': GuardUpCell,
    'v': GuardDownCell,
    '<': GuardLeftCell,
    '>': GuardRightCell
}


class PatrolMap:
    __slots__ = 'rows', 'live_cells'

    rows: list[str]
    live_cells: dict[tuple[int, int], Cell]

    def __init__(self, rows: list[str]):
        self.rows = rows
        self.live_cells = dict()
        for i, line in enumerate(self.rows):
            for j, value in enumerate(line):
                if value in GUARD_TYPES:
                    guard_type = GUARD_TYPES[value]
                    self.live_cells[(i, j)] = guard_type(self, i, j)

    def run(self) -> None:
        while self.step():
            #print('\n'.join(self.rows))
            #print('\n')
            pass

    def step(self) -> bool:
        current_live_cells = self.live_cells
        self.live_cells = dict()

        for cell in current_live_cells.values():
            cell.update()

        if self.live_cells:
            return True

    def replace(
        self, i: int, j: int, char: str, cell_type: Optional[type(Cell)] = None
    ) -> None:
        if 0 <= i < len(self.rows) and 0 <= j < len(self.rows[i]):
            self.rows[i] = replace_index(self.rows[i], j, char)

            if cell_type:
                cell = cell_type(self, i, j)
                self.live_cells[i, j] = cell

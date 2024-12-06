from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional

from lib.lineutils import replace_index


class Cell(ABC):
    __slots__ = 'board', 'i', 'j'

    board: Board
    i: int
    j: int

    def __init__(self, board: Board, i: int, j: int):
        self.board = board
        self.i = i
        self.j = j

    @abstractmethod
    def update(self):
        pass

    def _cell_up(self) -> Optional[str]:
        if self.i >= 0:
            return self.board.rows[self.i - 1][self.j]
        return None

    def _cell_down(self) -> Optional[str]:
        if self.i + 1 < len(self.board.rows):
            return self.board.rows[self.i + 1][self.j]
        return None

    def _cell_left(self) -> Optional[str]:
        row = self.board.rows[self.i]
        if self.j > 0:
            return row[self.j - 1]
        return None

    def _cell_right(self) -> Optional[str]:
        row = self.board.rows[self.i]
        if self.j + 1 < len(row):
            return row[self.j + 1]
        return None

    def _replace_self(
        self, char: str, cell_type: Optional[type(Cell)] = None
    ) -> None:
        self.board.replace(self.i, self.j, char, cell_type)

    def _replace_up(
        self, char: str, cell_type: Optional[type(Cell)] = None
    ) -> None:
        self.board.replace(self.i - 1, self.j, char, cell_type)

    def _replace_down(
        self, char: str, cell_type: Optional[type(Cell)] = None
    ) -> None:
        self.board.replace(self.i + 1, self.j, char, cell_type)

    def _replace_left(
        self, char: str, cell_type: Optional[type(Cell)] = None
    ) -> None:
        self.board.replace(self.i, self.j - 1, char, cell_type)

    def _replace_right(
        self, char: str, cell_type: Optional[type(Cell)] = None
    ) -> None:
        self.board.replace(self.i, self.j + 1, char, cell_type)


class Board:
    __slots__ = 'rows', 'live_cells'

    rows: list[str]
    live_cells: dict[tuple[int, int], Cell]

    def __init__(self, rows: list[str], cell_types: dict[str, type(Cell)]):
        self.rows = rows
        self.live_cells = dict()
        for i, line in enumerate(self.rows):
            for j, value in enumerate(line):
                if value in cell_types:
                    cell_type = cell_types[value]
                    self.live_cells[(i, j)] = cell_type(self, i, j)

    def run(self) -> None:
        while self.step():
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

from __future__ import annotations

from lib.common import grid_input

MAX_HEIGHT = 9

class TrailNode:
    __slots__ = 'pos', 'height', 'next_nodes'

    pos: tuple[int, int]
    height: int
    next_nodes: list[TrailNode]

    def __init__(self, pos: tuple[int, int], height: int):
        self.pos = pos
        self.height = height
        self.next_nodes = []

    def add_passable(self, next_node: TrailNode):
        if (next_node.height - self.height) == 1:
            self.next_nodes.append(next_node)

    def peaks(self) -> set[TrailNode]:
        if self.height == MAX_HEIGHT:
            return {self}
        peaks = set()
        for node in self.next_nodes:
            peaks.update(node.peaks())
        return peaks

    def describe(self, indent='') -> str:
        return (
            indent + f'Point {self.pos}, height {self.height}, next:\n'
            + ('\n'.join(
                node.describe(indent + '  ')
                for node in self.next_nodes
            ))
        )


@grid_input(int)
def get_trailhead_score(rows: list[list[int]]) -> int:
    trails = _read_trails(rows)
    return sum(len(node.peaks()) for node in trails)


@grid_input(int)
def get_trails(rows: list[list[int]]) -> str:
    trails = _read_trails(rows)
    return '\n'.join(trail.describe() for trail in trails)


def _read_trails(rows: list[list[int]]) -> list[TrailNode]:
    trailheads = []
    up_nodes = None
    for i, row in enumerate(rows):
        left_node = None
        current_nodes = []
        for j, cell in enumerate(row):
            node = TrailNode((i, j), cell)
            if up_nodes is not None:
                up_node = up_nodes[j]
                up_node.add_passable(node)
                node.add_passable(up_node)
            if left_node is not None:
                left_node.add_passable(node)
                node.add_passable(left_node)
            if cell == 0:
                trailheads.append(node)
            current_nodes.append(node)
            left_node = node
        up_nodes = current_nodes
    return trailheads

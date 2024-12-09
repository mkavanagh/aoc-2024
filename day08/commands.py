from collections import defaultdict
from typing import Callable, Generator

from lib.common import read_strings
from lib.lineutils import replace_index

Node = tuple[int, int]
Antennae = dict[str, list[Node]]
AntinodeGenerator: type = Callable[[Node, Node], Generator[Node, None, None]]
AntinodeGeneratorFactory: type = Callable[[int, int], AntinodeGenerator]


def get_antinode_uniques(filename: str) -> int:
    return _get_antinode_uniques(filename, _polar_antinode_generator)


def get_antinodes(filename: str) -> str:
    return _get_antinodes(filename, _polar_antinode_generator)


def get_resonant_antinode_uniques(filename: str) -> int:
    return _get_antinode_uniques(filename, _resonant_antinode_generator)


def get_resonant_antinodes(filename: str) -> str:
    return _get_antinodes(filename, _resonant_antinode_generator)


def _get_antinode_uniques(
    filename: str, generator_factory: AntinodeGeneratorFactory
) -> int:
    lines = read_strings(filename)
    i_max, j_max = len(lines), len(lines[0])
    antennae = _parse_antennae(lines)
    return len(set(_find_antinodes(antennae, generator_factory(i_max, j_max))))


def _get_antinodes(
    filename: str, generator_factory: AntinodeGeneratorFactory
) -> str:
    lines = read_strings(filename)
    i_max, j_max = len(lines), len(lines[0])
    antennae = _parse_antennae(lines)
    for i, j in _find_antinodes(antennae, generator_factory(i_max, j_max)):
        lines[i] = replace_index(lines[i], j, '#')
    return '\n'.join(lines)


def _parse_antennae(lines: list[str]) -> Antennae:
    antennae = defaultdict(list)
    for i, line in enumerate(lines):
        for j, char in enumerate(line):
            if char != '.':
                antennae[char].append((i, j))
    return antennae


def _find_antinodes(
    antennae: Antennae,
    generator: AntinodeGenerator
) -> list[Node]:
    antinodes = []
    for locations in antennae.values():
        for x, a in enumerate(locations):
            for b in locations[x + 1:]:
                antinodes.extend(node for node in generator(a, b))
    return antinodes


def _polar_antinode_generator(i_max: int, j_max: int) -> AntinodeGenerator:
    def _in_bounds(node: Node) -> bool:
        return 0 <= node[0] < i_max and 0 <= node[1] < j_max

    def _generator(node_1: Node, node_2: Node) -> Generator[Node, None, None]:
        delta_i, delta_j = node_2[0] - node_1[0], node_2[1] - node_1[1]

        antinode_1 = node_1[0] - delta_i, node_1[1] - delta_j
        if _in_bounds(antinode_1):
            yield antinode_1

        antinode_2 = node_2[0] + delta_i, node_2[1] + delta_j
        if _in_bounds(antinode_2):
            yield antinode_2

    return _generator


def _resonant_antinode_generator(i_max: int, j_max: int) -> AntinodeGenerator:
    def _in_bounds(node: Node) -> bool:
        return 0 <= node[0] < i_max and 0 <= node[1] < j_max

    def _generator(node_1: Node, node_2: Node) -> Generator[Node, None, None]:
        delta_i, delta_j = node_2[0] - node_1[0], node_2[1] - node_1[1]

        node = node_1
        while _in_bounds(node):
            yield node
            node = node[0] - delta_i, node[1] - delta_j

        node = node_2
        while _in_bounds(node):
            yield node
            node = node[0] + delta_i, node[1] + delta_j

    return _generator

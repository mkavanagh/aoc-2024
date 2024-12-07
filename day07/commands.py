from typing import Generator, Iterable

from lib.common import read_strings


def get_calibration(filename: str) -> int:
    equations = _parse_equations(read_strings(filename))
    return sum(equation[0] for equation in _solvable(equations))


def get_solvable(filename: str) -> str:
    equations = _parse_equations(read_strings(filename))
    return _describe(_solvable(equations))


def get_unsolvable(filename: str) -> str:
    equations = _parse_equations(read_strings(filename))
    return _describe(_unsolvable(equations))


def _parse_equations(lines: Iterable[str]) -> list[tuple[int, list[int]]]:
    return [
        (int(parts[0]), [int(x) for x in parts[1].split()])
        for parts in
        (
            line.split(':')
            for line in lines
        )
    ]


def _describe(equations: Iterable[tuple[int, list[int]]]) -> str:
    return '\n'.join(
        str(equation[0]) + ': ' + (', '.join(str(x) for x in equation[1]))
        for equation
        in equations
    )


def _solvable(
    equations: Iterable[tuple[int, list[int]]]
) -> Generator[tuple[int, list[int]], None, None]:
    return (
        equation
        for equation in equations
        if _can_satisfy(equation[0], equation[1])
    )


def _unsolvable(
    equations: Iterable[tuple[int, list[int]]]
) -> Generator[tuple[int, list[int]], None, None]:
    return (
        equation
        for equation in equations
        if not _can_satisfy(equation[0], equation[1])
    )


def _can_satisfy(
    target: int, operands: list[int], i: int = 0, acc: int = 0
) -> bool:
    if i == len(operands):
        return target == acc

    if i == 0:
        return _can_satisfy(target, operands, 1, operands[0])

    if target < acc:
        return False

    return (
        _can_satisfy(target, operands, i + 1, acc * operands[i])
        or _can_satisfy(target, operands, i + 1, acc + operands[i])
    )

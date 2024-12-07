from typing import Callable, Generator, Iterable

from lib.common import read_strings


class Solver:
    __slots__ = 'operators'

    operators: list[Callable[[int, int], int]]

    def __init__(self, operators):
        self.operators = operators

    def can_solve(
        self, target: int, operands: list[int], i: int = 0, acc: int = 0
    ) -> bool:
        if i == len(operands):
            return target == acc

        if i == 0:
            return self.can_solve(target, operands, 1, operands[0])

        if target < acc:
            return False

        return any(
            self.can_solve(target, operands, i + 1, operator(acc, operands[i]))
            for operator in self.operators
        )


default_operators = [lambda x, y: x + y, lambda x, y: x * y]
default_solver = Solver(default_operators)
concat_solver = Solver(default_operators + [lambda x, y: int(str(x) + str(y))])


def get_calibration(filename: str) -> int:
    equations = _parse_equations(read_strings(filename))
    return sum(equation[0] for equation in _solvable(equations, default_solver))


def get_solvable(filename: str) -> str:
    equations = _parse_equations(read_strings(filename))
    return _describe(_solvable(equations, default_solver))


def get_unsolvable(filename: str) -> str:
    equations = _parse_equations(read_strings(filename))
    return _describe(_unsolvable(equations, default_solver))


def get_calibration_concat(filename: str) -> int:
    equations = _parse_equations(read_strings(filename))
    return sum(
        equation[0]
        for equation in _solvable(equations, concat_solver)
    )


def get_solvable_concat(filename: str) -> str:
    equations = _parse_equations(read_strings(filename))
    return _describe(_solvable(equations, concat_solver))


def get_unsolvable_concat(filename: str) -> str:
    equations = _parse_equations(read_strings(filename))
    return _describe(_unsolvable(equations, concat_solver))


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
    equations: Iterable[tuple[int, list[int]]],
    solver: Solver
) -> Generator[tuple[int, list[int]], None, None]:
    return (
        equation
        for equation in equations
        if solver.can_solve(equation[0], equation[1])
    )


def _unsolvable(
    equations: Iterable[tuple[int, list[int]]],
    solver: Solver
) -> Generator[tuple[int, list[int]], None, None]:
    return (
        equation
        for equation in equations
        if not solver.can_solve(equation[0], equation[1])
    )

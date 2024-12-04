"""Advent of Code 2024, Day 3."""

from typing import Optional

from lib.common import read_binary


def get_mul(filename: str) -> int:
    """Parse and execute a "mul" program according to Day 3, Part 1."""
    program = read_binary(filename)
    parsed = _parse_mul(program)
    return sum(x * y for x, y in parsed)


def get_mul_conditional(filename: str) -> int:
    """
    Parse and execute a "mul with conditionals" program according to Day 3,
    Part 2.
    """
    program = read_binary(filename)
    parsed = _parse_conditional_mul(program)
    return sum(x * y for x, y in parsed)


def _parse_mul(program: bytes) -> list[tuple[int, int]]:
    i = 0
    results = []
    while i < len(program):
        if program[i] == ord(b'm'):
            i, mul = _consume_mul(program, i)
            if mul is not None:
                results.append(mul)
        else:
            i += 1
    return results


def _parse_conditional_mul(program: bytes) -> list[tuple[int, int]]:
    i = 0
    results = []
    mul_enabled = True
    while i < len(program):
        if mul_enabled and program[i] == ord(b'm'):
            i, mul = _consume_mul(program, i)
            if mul is not None:
                results.append(mul)
        elif program[i] == ord(b'd'):
            i, conditional = _consume_conditional(program, i)
            if conditional is not None:
                mul_enabled = conditional
        else:
            i += 1
    return results


def _consume_mul(
    program: bytes, i: int
) -> tuple[int, Optional[tuple[int, int]]]:
    if program.startswith(b'mul(', i):
        i, value_1 = _consume_number(program, i + len(b'mul('))
        if value_1 is None:
            return i, None

        if program[i] != ord(b','):
            return i, None

        i, value_2 = _consume_number(program, i + 1)
        if value_2 is None:
            return i, None

        if program[i] != ord(b')'):
            return i, None

        return i + 1, (value_1, value_2)
    return i + 1, None


def _consume_number(
    program: bytes, i: int
) -> tuple[int, Optional[int]]:
    matched = bytearray()
    while i < len(program) and program[i] in set(b'0123456789'):
        matched.append(program[i])
        i += 1

    value = None
    if len(matched) > 0:
        value = int(matched.decode(encoding='ascii'))

    return i, value


def _consume_conditional(
    program: bytes, i: int
) -> tuple[int, Optional[bool]]:
    if program.startswith(b'do()', i):
        return i + len(b'do()'), True

    if program.startswith(b'don\'t()', i):
        return i + len(b'don\'t()'), False

    return i + 1, None

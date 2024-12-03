#!/usr/bin/env python3

import argparse, sys
from typing import Optional

from lib.common import read_binary, read_columns, read_rows


def get_distance(filename: str) -> int:
    """Calculate the "distance" score from AoC 2024 Day 1, Part 1."""

    lists = read_columns(filename)

    distance = 0
    for l, r in zip(sorted(lists[0]), sorted(lists[1])):
        distance += abs(l - r)
    return distance


def get_similarity(filename: str) -> int:
    """Calculate the "similarity" score from AoC 2024 Day 1, Part 2."""

    lists = read_columns(filename)

    similarity = 0
    left, right = sorted(lists[0]), sorted(lists[1])
    left_index, right_index = 0, 0

    while left_index < len(left) and right_index < len(right):
        left_val = left[left_index]
        next_val = None

        # count consecutive occurrences of left value
        left_count = 1
        while left_index + 1 < len(left):
            left_index += 1
            next_val = left[left_index]
            if next_val > left_val:
                break
            else:
                left_count += 1

        # count consecutive matching occurrences of right value
        right_count = 0
        while right_index < len(right):
            right_val = right[right_index]
            if left_val < right_val:
                break
            elif left_val == right_val:
                right_count += 1
                right_index += 1
            elif left_val > right_val:
                right_index += 1

        similarity += left_val * left_count * right_count

        if next_val is None:
            return similarity


def get_sizes(filename: str) -> list[int]:
    """Count the number of values in each input list."""
    lists = read_columns(filename)
    return [len(x) for x in lists]


def get_uniques(filename: str) -> list[int]:
    """Count the number of unique values in each input list."""
    lists = read_columns(filename)
    return [len(set(x)) for x in lists]


def get_safe_count(filename: str) -> int:
    """
    Count the number of "safe reports" according to AoC 2024 Day 2, Part 1.
    """
    return sum(is_safe(report) for report in read_rows(filename))


def is_safe(report: list[int], use_dampener: bool=False) -> bool:
    """
    Checks if a report has "safe levels" according to AoC 2024 Day 2, Part 1.
    """
    last_sign = None
    for i in range(0, len(report) - 1):
        delta = report[i] - report[i+1]
        if not (1 <= abs(delta) <= 3):
            return use_dampener and (
                dampener(report, i)
                or dampener(report, i + 1)
             )
        sign = int(delta < 0)
        if last_sign is not None and last_sign != sign:
            return use_dampener and (
                dampener(report, i - 1)
                or dampener(report, i)
                or dampener(report, i + 1)
            )
        last_sign = sign
    return True


def dampener(report: list[int], i: int) -> bool:
    return is_safe(report[:i] + report[i+1:]) # cut out report[i]


def get_dampened_count(filename: str) -> int:
    """
    Count the number of "safe reports" after "dampening" according to AoC 2024
    Day 2, Part 2.
    """
    return sum(
        is_safe(report, True)
        for report in read_rows(filename)
    )


def get_mul(filename: str) -> int:
    program = read_binary(filename)
    parsed = parse_mul(program)
    return sum(x * y for x, y in parsed)


def get_conditional_mul(filename: str) -> int:
    program = read_binary(filename)
    parsed = parse_conditional_mul(program)
    return sum(x * y for x, y in parsed)


def parse_mul(program: bytes) -> list[tuple[int, int]]:
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


def parse_conditional_mul(program: bytes) -> list[tuple[int, int]]:
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
    else:
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
    elif program.startswith(b'don\'t()', i):
        return i + len(b'don\'t()'), False
    return i + 1, None


def main(argv: list[str]):
    parser = argparse.ArgumentParser()

    parser.add_argument('file')

    cmd_parsers = parser.add_subparsers(
        title='Available sub-commands',
        metavar='[command]',
        required=True
    )

    funcs = [
        get_distance, get_similarity, get_sizes, get_uniques,
        get_safe_count, get_dampened_count,
        get_mul, get_conditional_mul
    ]

    for func in funcs:
        cmd = func.__name__.removeprefix('get_')
        cmd_parser = cmd_parsers.add_parser(cmd, help=func.__doc__)
        cmd_parser.set_defaults(func=func)

    args = parser.parse_args(argv[1:])

    print(args.func(args.file))


if __name__ == '__main__':
    main(sys.argv)

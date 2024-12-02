#!/usr/bin/env python3

import argparse


def read_columns(filename: str) -> list[list[int]]:
    """Read a file containing columnar lists of integers (with equal length)."""
    lists = []
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            for i, x in enumerate(line.split()):
                if i == len(lists):
                    lists.append([])
                lists[i].append(int(x))
    return lists


def read_rows(filename: str) -> list[list[int]]:
    """Read a file containing rows of integers, one row per line."""
    with open(filename, 'r', encoding='utf-8') as file:
        return [
            [int(x) for x in line.split()]
            for line in file
        ]


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


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('file')

    cmd_parsers = parser.add_subparsers(
        title='Available sub-commands',
        metavar='[command]',
        required=True
    )

    funcs = [
        get_distance, get_similarity, get_sizes, get_uniques,
        get_safe_count, get_dampened_count
    ]

    for func in funcs:
        cmd = func.__name__.removeprefix('get_')
        cmd_parser = cmd_parsers.add_parser(cmd, help=func.__doc__)
        cmd_parser.set_defaults(func=func)

    args = parser.parse_args()

    print(args.func(args.file))


if __name__ == '__main__':
    main()

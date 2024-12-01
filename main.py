#!/usr/bin/env python3

import argparse


def read_lists(filename: str) -> list[list[int]]:
    lists = [[], []]
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            (l, r) = line.split()
            lists[0].append(int(l))
            lists[1].append(int(r))
    return lists


def get_distance(left: list[int], right: list[int]) -> int:
    """Calculate the "distance" score from AoC 2024 Day 1, Part 1."""
    distance = 0
    for l, r in zip(sorted(left), sorted(right)):
        distance += abs(l - r)
    return distance


def get_similarity(left: list[int], right: list[int]) -> int:
    """Calculate the "similarity" score from AoC 2024 Day 1, Part 2."""
    similarity = 0
    left, right = sorted(left), sorted(right)
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


def get_sizes(left: list, right: list) -> tuple[int, int]:
    """Count the number of values in each input list."""
    return len(left), len(right)


def get_uniques(left: list, right: list) -> tuple[int, int]:
    """Count the number of unique values in each input list."""
    return len(set(left)), len(set(right))


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('file')

    cmd_parsers = parser.add_subparsers(
        title='Available sub-commands',
        metavar='[command]',
        required=True
    )

    for func in [get_distance, get_similarity, get_sizes, get_uniques]:
        cmd = func.__name__.removeprefix('get_')
        cmd_parser = cmd_parsers.add_parser(cmd, help=func.__doc__)
        cmd_parser.set_defaults(func=func)

    args = parser.parse_args()

    (left, right) = read_lists(args.file)

    print(args.func(left, right))


if __name__ == '__main__':
    main()

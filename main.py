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
    distance = 0
    for l, r in zip(sorted(left), sorted(right)):
        distance += abs(l - r)
    return distance


def get_sizes(left: list, right: list) -> tuple[int, int]:
    return len(left), len(right)


def get_uniques(left: list, right: list) -> tuple[int, int]:
    return len(set(left)), len(set(right))


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('file')

    cmd_parsers = parser.add_subparsers(required=True)

    for func in [get_distance, get_sizes, get_uniques]:
        cmd = func.__name__.removeprefix('get_')
        cmd_parser = cmd_parsers.add_parser(cmd)
        cmd_parser.set_defaults(func=func)

    args = parser.parse_args()

    (left, right) = read_lists(args.file)

    print(args.func(left, right))


if __name__ == '__main__':
    main()

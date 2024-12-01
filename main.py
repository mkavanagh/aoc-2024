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


def get_sizes(left: list, right: list) -> list[int]:
    return [len(left), len(right)]


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('file')

    cmds = parser.add_subparsers(required=True)

    distance_cmd = cmds.add_parser('distance')
    distance_cmd.set_defaults(func=get_distance)

    sizes_cmd = cmds.add_parser('sizes')
    sizes_cmd.set_defaults(func=get_sizes)

    args = parser.parse_args()

    (left, right) = read_lists(args.file)

    print(args.func(left, right))


if __name__ == '__main__':
    main()

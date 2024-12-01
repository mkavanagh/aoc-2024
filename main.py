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


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('file')

    subparsers = parser.add_subparsers()
    distance_cmd = subparsers.add_parser('distance')
    distance_cmd.set_defaults(func=get_distance)

    args = parser.parse_args()

    (left, right) = read_lists(args.file)

    print(args.func(left, right))


if __name__ == '__main__':
    main()

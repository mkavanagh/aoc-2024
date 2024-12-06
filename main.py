#!/usr/bin/env python3
"""Solutions to Advent of Code 2024 - main entrypoint."""

import argparse
import sys

from day01.commands import get_distance, get_similarity
from day02.commands import get_safe_count, get_dampened_count
from day03.commands import get_mul, get_mul_conditional
from day04.commands import get_xmas_count, get_masx_count
from lib.commands import get_sizes, get_uniques


def main(argv: list[str]):
    """
    Main entrypoint - parse command line arguments and invoke run function.
    """
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
        get_mul, get_mul_conditional,
        get_xmas_count, get_masx_count
    ]

    for func in funcs:
        cmd = func.__name__.removeprefix('get_')
        cmd_parser = cmd_parsers.add_parser(cmd, help=func.__doc__)
        cmd_parser.set_defaults(func=func)

    args = parser.parse_args(argv[1:])

    print(args.func(args.file))


if __name__ == '__main__':
    main(sys.argv)

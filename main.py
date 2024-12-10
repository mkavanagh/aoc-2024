#!/usr/bin/env python3
"""Solutions to Advent of Code 2024 - main entrypoint."""

import argparse
import sys

from lib.common import collect_commands


def main(argv: list[str]):
    """
    Main entrypoint - parse command line arguments and invoke run function.
    """
    parser = argparse.ArgumentParser()

    cmd_parsers = parser.add_subparsers(
        title='Available sub-commands',
        description='''
To get help with a specific sub-command, use: %(prog)s [command] -h
''',
        metavar='[command]',
        required=True
    )

    with collect_commands() as funcs:
        __import__('lib.commands')
        __import__('day01.commands')
        __import__('day02.commands')
        __import__('day03.commands')
        __import__('day04.commands')
        __import__('day05.commands')
        __import__('day06.commands')
        __import__('day07.commands')
        __import__('day08.commands')
        __import__('day09.commands')

        for func in funcs:
            cmd = func.__name__.removeprefix('get_')
            cmd_parser = cmd_parsers.add_parser(cmd, help=func.__doc__)
            cmd_parser.add_argument('file', nargs='?')
            cmd_parser.set_defaults(func=func)

    args = parser.parse_args(argv[1:])

    print(args.func(args.file))


if __name__ == '__main__':
    main(sys.argv)

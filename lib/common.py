"""Common utilities (IO etc)."""
import io
import sys
from functools import wraps
from typing import BinaryIO, TextIO, Union


def column_input(value_type):
    """Read a file containing columnar lists (with equal length)."""
    def decorator(func):
        @wraps(func)
        def decorated(filename, *args):
            columns = []
            with _open_text_input(filename) as input_file:
                for line in input_file:
                    for i, x in enumerate(line.split()):
                        if i == len(columns):
                            columns.append([])
                        columns[i].append(value_type(x))
            return func(columns, *args)
        return decorated
    return decorator


def row_input(value_type):
    """Read a file containing rows, one row per line."""
    def decorator(func):
        @wraps(func)
        def decorated(filename, *args):
            with _open_text_input(filename) as input_file:
                return func(
                    [
                        [int(x) for x in line.split()]
                        for line in input_file
                    ],
                    *args
                )
        return decorated
    return decorator


def line_input():
    """Read a text file as a list of strings, one per line."""
    def decorator(func):
        @wraps(func)
        def decorated(filename, *args):
            with _open_text_input(filename) as input_file:
                return func(
                    [line.rstrip('\n') for line in input_file],
                    *args
                )
        return decorated
    return decorator


def binary_input():
    """Read a binary file as bytes."""
    def decorator(func):
        @wraps(func)
        def decorated(filename, *args):
            with _open_binary_input(filename) as input_file:
                return func(input_file.read(), *args)
        return decorated
    return decorator


def _open_text_input(filename : Union[None, str]) -> TextIO:
    if filename is None:
        return io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')
    return open(filename, 'r', encoding='utf-8')


def _open_binary_input(filename : Union[None, str]) -> BinaryIO:
    if filename is None:
        return sys.stdin.buffer
    return open(filename, 'b', encoding='utf-8')

"""Utility commands."""

from lib.common import read_columns


def get_sizes(filename: str) -> list[int]:
    """Count the number of values in each input list."""
    lists = read_columns(filename)
    return [len(x) for x in lists]


def get_uniques(filename: str) -> list[int]:
    """Count the number of unique values in each input list."""
    lists = read_columns(filename)
    return [len(set(x)) for x in lists]

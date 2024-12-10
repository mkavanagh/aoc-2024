"""Utility commands."""

from lib.common import column_input


@column_input(int)
def get_column_sizes(columns: list[list[int]]) -> list[int]:
    """Count the number of values in each input colu,n."""
    return [len(column) for column in columns]


@column_input(int)
def get_column_uniques(columns: list[list[int]]) -> list[int]:
    """Count the number of unique values in each input column."""
    return [len(set(column)) for column in columns]

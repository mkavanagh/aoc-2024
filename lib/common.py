"""Common utilities (IO etc)."""


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


def read_binary(filename: str) -> bytes:
    """Read a binary file as bytes."""
    with open(filename, 'rb') as file:
        return file.read()


def read_strings(filename: str) -> list[str]:
    """Read a text file as a list of strings, one per line."""
    with open(filename, 'r') as file:
        return [line.rstrip('\n') for line in file]

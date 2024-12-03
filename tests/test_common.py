import os

from main import read_binary, read_columns, read_rows

dirname = os.path.dirname(__file__)


def test_read_binary():
    empty = read_binary(dirname + '/data/empty')
    assert empty == b''

    example = read_binary(dirname + '/data/example.bin')
    assert example == b'hello world'


def test_read_columns():
    empty = read_columns(dirname + '/data/empty')
    assert empty == []

    columns = read_columns(dirname + '/data/columns.txt')
    assert columns == [[1, 2, 3, 4], [5, 6, 7], [8, 9]]


def test_read_rows():
    empty = read_rows(dirname + '/data/empty')
    assert empty == []

    rows = read_rows(dirname + '/data/rows.txt')
    assert rows == [[1, 2, 3], [4, 5], [6, 7, 8, 9]]
import os

from lib.common import read_binary, read_columns, read_rows, read_strings

test_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
data_path = os.path.join(test_root, 'data', 'common')


def test_read_binary():
    print(f'data_path: {data_path}, {__file__}')
    empty = read_binary(data_path + '/empty')
    assert empty == b''

    example = read_binary(data_path + '/example.bin')
    assert example == b'hello world'


def test_read_columns():
    empty = read_columns(data_path + '/empty')
    assert empty == []

    columns = read_columns(data_path + '/columns.txt')
    assert columns == [[1, 2, 3, 4], [5, 6, 7], [8, 9]]


def test_read_rows():
    empty = read_rows(data_path + '/empty')
    assert empty == []

    rows = read_rows(data_path + '/rows.txt')
    assert rows == [[1, 2, 3], [4, 5], [6, 7, 8, 9]]


def test_read_strings():
    empty = read_strings(data_path + '/empty')
    assert empty == []

    strings = read_strings(data_path + '/strings.txt')
    assert strings == ["hello", "world"]

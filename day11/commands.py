from lib.common import row_input


@row_input(int)
def get_blink_25(rows: list[list[int]]) -> int:
    return sum(
        _blink_x(stone, 25, dict())
        for stone in rows[0]
    )


@row_input(int)
def get_blink_75(rows: list[list[int]]) -> int:
    return sum(
        _blink_x(stone, 75, dict())
        for stone in rows[0]
    )


def _blink_x(initial: int, x: int, memo: dict[tuple[int, int], int]) -> int:
    if x == 0:
        return 1

    x -= 1

    if initial == 0:
        return _blink_x(1, x, memo)

    if (initial, x) in memo:
        return memo[initial, x]

    str_value = str(initial)
    digits = len(str_value)
    if digits % 2 == 0:
        split = int(digits / 2)
        left = int(str_value[:split])
        right = int(str_value[split:])
        value = _blink_x(int(left), x, memo) + _blink_x(int(right), x, memo)
    else:
        value = _blink_x(initial * 2024, x, memo)

    memo[initial, x] = value

    return value

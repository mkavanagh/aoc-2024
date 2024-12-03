"""Advent of Code 2024, Day 2"""

from lib.common import read_rows


def get_safe_count(filename: str) -> int:
    """
    Count the number of "safe reports" according to Part 1.
    """
    return sum(_is_safe(report) for report in read_rows(filename))


def _is_safe(report: list[int], use_dampener: bool=False) -> bool:
    last_sign = None
    for i in range(0, len(report) - 1):
        delta = report[i] - report[i+1]
        if not (1 <= abs(delta) <= 3):
            return use_dampener and (
                _dampener(report, i)
                or _dampener(report, i + 1)
            )
        sign = int(delta < 0)
        if last_sign is not None and last_sign != sign:
            return use_dampener and (
                _dampener(report, i - 1)
                or _dampener(report, i)
                or _dampener(report, i + 1)
            )
        last_sign = sign
    return True


def _dampener(report: list[int], i: int) -> bool:
    return _is_safe(report[:i] + report[i + 1:]) # cut out report[i]


def get_dampened_count(filename: str) -> int:
    """
    Count the number of "safe reports" after "dampening" according to Part 2.
    """
    return sum(
        _is_safe(report, True)
        for report in read_rows(filename)
    )

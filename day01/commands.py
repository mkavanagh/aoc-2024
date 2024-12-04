"""Advent of Code 2024, Day 1"""

from lib.common import read_columns


def get_distance(filename: str) -> int:
    """Calculate the "distance" score from Day 1, Part 1."""

    lists = read_columns(filename)

    distance = 0
    for l, r in zip(sorted(lists[0]), sorted(lists[1])):
        distance += abs(l - r)
    return distance


def get_similarity(filename: str) -> int:
    """Calculate the "similarity" score from Day 1, Part 2."""

    lists = read_columns(filename)

    similarity = 0
    left, right = sorted(lists[0]), sorted(lists[1])
    left_index, right_index = 0, 0

    while left_index < len(left) and right_index < len(right):
        left_val = left[left_index]
        next_val = None

        # count consecutive occurrences of left value
        left_count = 1
        while left_index + 1 < len(left):
            left_index += 1
            next_val = left[left_index]

            if next_val > left_val:
                break

            left_count += 1

        # count consecutive matching occurrences of right value
        right_count = 0
        while right_index < len(right):
            right_val = right[right_index]

            if left_val < right_val:
                break

            if left_val == right_val:
                right_count += 1
                right_index += 1
            elif left_val > right_val:
                right_index += 1

        similarity += left_val * left_count * right_count

        if next_val is None:
            return similarity

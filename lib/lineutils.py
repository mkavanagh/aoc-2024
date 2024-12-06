def transpose(lines: list[str]) -> list[str]:
    if not lines:
        return []

    transposed = ['' for _ in range(0, len(lines[0]))]
    for line in lines:
        for i in range(0, len(line)):
            transposed[-(i + 1)] += line[i]
    return transposed


def flip(lines: list[str]) -> list[str]:
    flipped = list(lines)
    flipped.reverse()
    return flipped


def replace_index(line: str, i: int, replacement: str) -> str:
    return line[:i] + replacement + line[i + 1:]

from lib.common import line_input


@line_input()
def get_disk_blocks(lines: list[str]) -> str:
    """Show a representation of the disk blocks for Day 8."""
    return _parse_blocks(lines[0])


def _parse_blocks(disk_map: str) -> str:
    return ''.join(
        str(int(i / 2)) * int(value)
        if i % 2 == 0
        else '.' * int(value)
        for i, value in enumerate(disk_map)
    )

from lib.common import line_input


class Block:
    __slots__ = ('id', 'length', 'tail')

    id: int
    length: int
    tail: int

    def __init__(self, id, length, tail):
        self.id = id
        self.length = length
        self.tail = tail

    def describe(self) -> str:
        return (str(self.id) * self.length) + ('.' * self.tail)


@line_input()
def get_disk_blocks(lines: list[str]) -> str:
    """Show a representation of the disk blocks for Day 8."""
    return _describe_blocks(_parse_blocks(lines[0]))


def _parse_blocks(disk_map: str) -> list[Block]:
    lengths = disk_map[::2]
    tails = disk_map[1::2]
    if len(tails) < len(lengths):
        tails += '0'

    return [
        Block(str(i), int(lengths[i]), int(tails[i]))
        for i in range(0, int((len(disk_map) + 1) / 2))
    ]


def _describe_blocks(blocks: list[Block]) -> str:
    return ''.join(block.describe() for block in blocks)

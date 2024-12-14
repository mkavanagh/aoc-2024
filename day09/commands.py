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

    def checksum(self, offset: int) -> int:
        end_offset = (offset + self.length) - 1
        factor = int(
            (
                (offset + end_offset)
                * ((end_offset - offset) + 1)
            ) / 2
        )
        return self.id * factor


@line_input()
def get_disk_blocks(lines: list[str]) -> str:
    """Show a representation of the disk blocks for Day 8."""
    return _describe_blocks(_parse_disk_map(lines[0]))


@line_input()
def get_packed_checksum(lines: list[str]) -> int:
    return _checksum(_pack_blocks(_parse_disk_map(lines[0])))


@line_input()
def get_defragged_checksum(lines: list[str]) -> int:
    return _checksum(_defrag_blocks(_parse_disk_map(lines[0])))


@line_input()
def get_defragged(lines: list[str]) -> str:
    return _describe_blocks(_defrag_blocks(_parse_disk_map(lines[0])))


def _parse_disk_map(disk_map: str) -> list[Block]:
    lengths = disk_map[::2]
    tails = disk_map[1::2]
    if len(tails) < len(lengths):
        tails += '0'

    return [
        Block(i, int(lengths[i]), int(tails[i]))
        for i in range(0, int((len(disk_map) + 1) / 2))
    ]


def _describe_blocks(blocks: list[Block]) -> str:
    return ''.join(block.describe() for block in blocks)


def _pack_blocks(blocks: list[Block]) -> list[Block]:
    if not blocks:
        return blocks

    disk_tail = 0

    i = 0
    while i + 1 < len(blocks) > 1:
        source = blocks[-1]
        dest = blocks[i]

        to_move = min(source.length, dest.tail)

        if to_move:
            moved = Block(source.id, to_move, dest.tail - to_move)
            blocks.insert(i + 1, moved)

            dest.tail = 0
            source.length -= to_move
            disk_tail += to_move

            if source.length == 0:
                blocks.pop()
                disk_tail += source.tail

        i += 1

    blocks[-1].tail += disk_tail

    return blocks


def _defrag_blocks(blocks: list[Block]) -> list[Block]:
    if not blocks:
        return blocks

    i = len(blocks) - 1
    first_free = 0
    while i > 0:
        source = blocks[i]
        to_move = source.length
        seen_free = False
        for j in range(first_free, i):
            dest = blocks[j]
            if dest.tail and not seen_free:
                seen_free = True
                first_free = j
            if dest.tail >= to_move:
                moved = Block(source.id, to_move, dest.tail - to_move)
                blocks.insert(j + 1, moved)
                i += 1

                dest.tail = 0

                del blocks[i]
                blocks[i - 1].tail += source.length + source.tail

                break
        i -= 1

    return blocks


def _checksum(blocks: list[Block]) -> int:
    checksum = 0
    offset = 0
    for block in blocks:
        checksum += block.checksum(offset)
        offset += block.length + block.tail
    return checksum
